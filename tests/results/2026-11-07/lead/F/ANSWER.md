# Backend Technical Specification: การตัดสินคำขอ

สถานะ: เอกสารออกแบบจากหลักฐานปัจจุบัน ยังไม่ได้พัฒนา rejection

## ขอบเขตและหลักฐาน

เอกสารนี้ใช้สำหรับผู้พัฒนา backend เพื่อเพิ่มการปฏิเสธคำขอโดย manager โดยรักษาพฤติกรรม approval และ payload ของผู้เรียกเดิม ตาม [requirements.md](/tmp/panda-suite-evals-lead/F/requirements.md:3) ขอบเขตคือ Python function; fixture ไม่มี HTTP server, network interface หรือ persistence จึงไม่มีหลักฐานสำหรับกำหนด route, database, retention หรือ deployment architecture

## พฤติกรรมปัจจุบัน

จาก [service.py](/tmp/panda-suite-evals-lead/F/service.py:4):

| เงื่อนไข | ผลปัจจุบัน |
| --- | --- |
| `actor["role"] != "manager"` | `PermissionError("manager required")` ตรวจเป็นลำดับแรก |
| manager และ `request["status"] != "pending"` | `ValueError("request must be pending")` |
| manager และสถานะ pending | คืน mapping ใหม่ โดยคงข้อมูลเดิม เปลี่ยน `status` เป็น `approved` และเขียน `reviewer_id` ด้วย `actor["id"]` |

`approve(request, actor)` อ่าน key ด้วยการเข้าถึงโดยตรง ไม่มี schema/type validation; key ที่จำเป็นขาดอาจเกิด `KeyError` ตามเส้นทางที่ทำงาน ไม่มีการเปลี่ยน mapping ต้นทางโดยตรง แต่การ copy เป็น shallow copy จึงไม่ได้แยก nested object ออกจากกัน ไม่มีการบันทึกหรือควบคุม concurrency

`label(request)` คืนข้อความ `<id>: <status>` โดยอ่านสอง key นั้น ไม่มีการตรวจสถานะ ([service.py](/tmp/panda-suite-evals-lead/F/service.py:12)) ไม่มีฟังก์ชัน rejection ใน source ปัจจุบัน การส่ง approved/rejected เข้า `approve` จะไม่ผ่านเงื่อนไข pending

## การออกแบบที่เสนอ

เพิ่มฟังก์ชัน `reject(request, actor, reason)` เป็น **ข้อเสนอ interface** เพื่อไม่เปลี่ยน signature หรือ payload ของ `approve` เดิม:

- อนุญาตเฉพาะ manager และคำขอ pending ตรวจสิทธิ์ก่อนสถานะ เช่นเดียวกับ approval
- เมื่อสำเร็จ คืน mapping ใหม่ที่คง field ของ request พร้อม `status="rejected"`, `reviewer_id=actor["id"]` และ field `rejection_reason` ที่เก็บ reason; ชื่อ field ใหม่นี้เป็นข้อเสนอ ยังไม่มีใน source
- ต้องมี reason ที่ไม่ว่าง ตาม requirement; ข้อเสนอ validation คือรับ string และถือว่า `reason.strip()` ต้องไม่ว่าง โดยไม่แก้ข้อความก่อนจัดเก็บ ทั้งกฎ whitespace/type และการจัดเก็บข้อความต้องยืนยันก่อนนำไปใช้
- ใช้ `PermissionError("manager required")` สำหรับผู้ไม่มีสิทธิ์ และ `ValueError("request must be pending")` สำหรับสถานะอื่น เพื่อสอดคล้องกับ approval; เสนอ `ValueError("rejection reason required")` สำหรับ reason ไม่ผ่าน validation ข้อความใหม่นี้ยังไม่ใช่ error ที่ระบบมีอยู่
- approved และ rejected เป็นสถานะสิ้นสุด ห้าม approve/reject ซ้ำผ่านฟังก์ชันเหล่านี้ การตัดสินซ้ำไม่ถือว่าสำเร็จแบบ idempotent; ไม่มีข้อเสนอให้แก้พฤติกรรม `label`

ตัวอย่างเชิงออกแบบเท่านั้น: request `{"id": 1, "status": "pending"}`, actor `{"id": 2, "role": "manager"}`, reason `"ข้อมูลไม่ครบ"` จะได้ `{"id": 1, "status": "rejected", "reviewer_id": 2, "rejection_reason": "ข้อมูลไม่ครบ"}` หากข้อเสนอ contract นี้ได้รับการยืนยัน

ไม่เพิ่ม network/storage ในขอบเขตนี้ ฟังก์ชันไม่สามารถรับประกัน atomic transition ของคำขอที่แชร์กันระหว่างผู้เรียกได้ หากภายหลังต้อง persist จะต้องมีข้อกำหนดแยกเรื่อง transaction และ concurrent decisions

## การตรวจสอบ

ดำเนินการแล้ว: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v` ผ่าน 2 tests ที่มีอยู่ ได้แก่ manager อนุมัติ pending และ member ถูกปฏิเสธ หลักฐานนี้ยืนยันเฉพาะกรณี approval ที่ทดสอบ ไม่ยืนยัน rejection

การตรวจที่เสนอสำหรับงานพัฒนา ยังไม่ได้เขียนหรือรัน:

- approval เดิมยังได้ผลและ error เดิม รวมถึงการคง field/payload และไม่เปลี่ยน request ต้นทาง
- manager ปฏิเสธ pending พร้อม reason ที่ผ่านกฎได้ และเก็บ reviewer/reason ตาม contract ที่ยืนยัน
- non-manager ปฏิเสธไม่ได้; reason ว่าง/whitespace/ชนิดไม่รองรับเป็นไปตามข้อสรุป validation
- approved/rejected ไม่สามารถเปลี่ยนผ่าน approve หรือ reject ได้ และ error precedence ยังคงสิทธิ์ก่อนสถานะ

## ข้อที่ยังตัดสินใจไม่ได้

| ประเด็น | สิ่งที่ต้องยืนยันและผลกระทบ | ขัดขวางการพัฒนาหรือไม่ |
| --- | --- | --- |
| Rejection contract | ผู้รับผิดชอบ requirement ต้องยืนยันชื่อ `reject`, `rejection_reason`, type/whitespace/การเก็บ reason และ error ใหม่; ไม่มีผู้รับผิดชอบที่ระบุชื่อใน fixture | ขัดขวางการสรุป public contract ของ rejection |
| Self-approval/rejection | ไม่มีหลักฐานว่าผู้ส่งคำขอตัดสินคำขอตนเองได้หรือไม่ และยังไม่มี field ระบุผู้ส่งในตัวอย่าง | ขัดขวางเฉพาะการเพิ่มกฎนี้; ไม่เพิ่มโดยสมมติ |
| HTTP, storage, retention | ไม่มี requirement หรือ implementation รองรับ | ไม่ขัดขวางส่วนฟังก์ชัน; อยู่นอกขอบเขตนี้ |

จัดทำเฉพาะเอกสาร ไม่มีการแก้ implementation หรือ tests

