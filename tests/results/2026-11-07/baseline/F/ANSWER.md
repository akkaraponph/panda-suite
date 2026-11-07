# Backend Technical Specification: การอนุมัติและปฏิเสธคำขอ

สถานะเอกสาร: อธิบายระบบปัจจุบันและเสนอการเพิ่มความสามารถ ยังไม่ได้แก้ไข source code

## ขอบเขตและหลักฐาน

อ้างอิง `service.py:1–13`, `requirements.md:3–7` และ `test_service.py:7–14` ระบบในชุดไฟล์นี้เป็นฟังก์ชัน Python ไม่มี HTTP server, network interface หรือ persistence เป้าหมายคือเพิ่มการปฏิเสธคำขอโดย manager พร้อมเหตุผล โดยรักษาพฤติกรรมอนุมัติและ payload ของผู้เรียกเดิม

## พฤติกรรมปัจจุบันที่ยืนยันจากโค้ด

`approve(request, actor)` รับ mapping สองตัว โดยอ่าน `actor["role"]` ก่อน หากไม่เท่ากับ `"manager"` จะยก `PermissionError("manager required")` จากนั้นตรวจ `request["status"]` ซึ่งต้องเท่ากับ `"pending"` มิฉะนั้นยก `ValueError("request must be pending")` เมื่อผ่านทั้งสองข้อจะคืน dict ใหม่ที่คัดลอกทุก key จาก request แล้วแทนค่า `status` เป็น `"approved"` และ `reviewer_id` เป็น `actor["id"]` (`service.py:4–9`)

ฟังก์ชันไม่แก้ request ต้นทาง แต่เป็นการคัดลอกแบบ shallow จึงไม่ได้แยก nested object ออกจากต้นฉบับ ค่า `reviewer_id` ที่มีอยู่จะถูกเขียนทับในผลลัพธ์ ไม่มีการตรวจชนิดข้อมูลหรือ schema โดยเฉพาะ การเข้าถึง key ที่ขาดอาจเกิด `KeyError`; ไม่ควรถือเป็น error contract ที่ออกแบบไว้

สถานะใดที่ไม่ใช่ pending รวมถึง approved และ rejected จะอนุมัติไม่ได้ในปัจจุบัน ยังไม่มีฟังก์ชัน reject และไม่มีการบันทึกการตัดสินใจลงฐานข้อมูล ไม่มีการตรวจว่า actor เป็นเจ้าของคำขอหรือไม่

`label(request)` คืนข้อความรูปแบบ `<id>: <status>` จากค่าที่ให้มา โดยไม่เปลี่ยนสถานะหรือแปลงชื่อสถานะ (`service.py:12–13`)

## ข้อกำหนดการเปลี่ยนแปลง

1. manager สามารถปฏิเสธคำขอได้ และต้องมีเหตุผลที่ไม่ว่าง (`requirements.md:3–4`)
2. approved และ rejected เป็นสถานะสิ้นสุด ห้ามตัดสินใจซ้ำหรือเปลี่ยนไปอีกสถานะผ่าน service นี้ (`requirements.md:4`)
3. คง signature, ลำดับการตรวจ, exception และผลลัพธ์ของ `approve(request, actor)` เดิม รวมถึง key ของผู้เรียกที่ไม่ได้เกี่ยวกับการตัดสินใจ (`requirements.md:5`)

## การออกแบบที่เสนอ — ยังไม่ได้ implement

เพิ่มฟังก์ชัน `reject(request, actor, reason)` โดยไม่เปลี่ยนการเรียก approve เดิม ข้อเสนอนี้เป็น API ภายใน Python ไม่ใช่ HTTP endpoint

| สถานะปัจจุบัน | approve โดย manager | reject โดย manager พร้อมเหตุผลที่ผ่านเกณฑ์ |
|---|---|---|
| pending | approved | rejected |
| approved | ปฏิเสธการทำงาน | ปฏิเสธการทำงาน |
| rejected | ปฏิเสธการทำงาน | ปฏิเสธการทำงาน |
| ค่าอื่น | คง ValueError เดิม | เสนอให้ปฏิเสธการทำงาน |

สำหรับ reject เสนอให้ตรวจ role ก่อน แล้วตรวจ status จากนั้นตรวจ reason เพื่อให้สอดคล้องกับแนวทาง approve ผู้ที่ role ไม่ใช่ manager ต้องไม่ได้ผลลัพธ์การตัดสินใจ แม้เหตุผลถูกต้อง ข้อเสนอ error สำหรับสองขั้นแรกคือ `PermissionError("manager required")` และ `ValueError("request must be pending")` ส่วน reason ที่ไม่ผ่านเกณฑ์เสนอ `ValueError` โดยข้อความต้องกำหนดเมื่อได้ข้อสรุปเรื่องรูปแบบเหตุผล

ผลลัพธ์ที่เสนอคือ dict ใหม่จาก request พร้อม `status="rejected"`, `reviewer_id=actor["id"]` และ field เหตุผลที่ต้องตกลงชื่อก่อน implement เช่น `rejection_reason` เก็บ field อื่นทั้งหมดไว้ตามเดิม ไม่เพิ่ม timestamp, ประวัติ audit หรือ metadata อื่นที่ยังไม่มีข้อกำหนด หาก field เหตุผลชนกับ key เดิมของผู้เรียก ต้องตกลงการจัดการก่อนเพื่อไม่ทำลาย payload เดิม

ไม่จำเป็นต้องเปลี่ยน label เพราะสามารถแสดงสถานะ rejected ที่ได้รับมาอยู่แล้ว ไม่เสนอการเปลี่ยนการอนุมัติให้ต้องมีเหตุผลหรือเปลี่ยนรูปแบบ payload เดิม

## สิ่งที่ยังตัดสินใจไม่ได้

| ประเด็น | เหตุที่ต้องยืนยัน |
|---|---|
| ชนิดและความหมายของ “เหตุผลไม่ว่าง” | ยังไม่ระบุว่าจะรับเฉพาะ string หรือไม่ และข้อความ whitespace ล้วนถือว่าว่างหรือไม่ |
| การเก็บและจำกัดเหตุผล | ยังไม่ทราบว่าจะ trim ก่อนเก็บหรือเก็บตามต้นฉบับ รวมถึงความยาวสูงสุด |
| ชื่อ field เหตุผลและกรณี key ชน | ต้องรักษา payload เดิม จึงไม่ควรเลือกชื่อและพฤติกรรมเขียนทับโดยไม่มีข้อสรุป |
| Validation ของ input ที่ผิด schema | โค้ดเดิมไม่มี validation เฉพาะ ต้องกำหนดขอบเขตเพิ่มเติมหากต้องการ error contract ที่แน่นอน |
| Self-approval / self-rejection | ไม่มีหลักฐานเรื่องกฎนี้ การไม่ตรวจในโค้ดปัจจุบันไม่ได้ยืนยันว่าเป็นนโยบายที่อนุญาต |
| HTTP routes, storage technology และ retention | ไม่มี network/persistence และข้อกำหนดระบุห้ามเลือกโดยไร้หลักฐาน จึงยังไม่กำหนด |
| การตัดสินใจพร้อมกัน | fixture ไม่มี state store หรือ transaction; การรับประกัน terminal state ระหว่างหลายผู้เรียกต้องออกแบบพร้อม persistence ในอนาคต |

## เกณฑ์ตรวจรับและการยืนยัน

ทดสอบเดิมด้วย `python3 -B -m unittest -v`: ผ่าน 2 tests คือ manager อนุมัติ pending ได้ และ member อนุมัติไม่ได้ ผลนี้ยังไม่ครอบคลุมความสามารถ reject

เมื่อข้อที่ค้างได้ข้อสรุปและเริ่ม implement ต้องตรวจอย่างน้อย: manager ปฏิเสธ pending พร้อมเหตุผลได้, non-manager ถูกปฏิเสธ, reason ว่างและ whitespace ตามกฎที่ตกลงถูกจัดการถูกต้อง, approved/rejected เปลี่ยนสถานะต่อไม่ได้ทั้ง approve และ reject, approve เดิมให้ผลเหมือนเดิม, key อื่นและ nested payload ยังอยู่, request ต้นทางไม่ถูกแก้, reviewer_id เป็น actor ผู้ตัดสินใจ และ label แสดงสถานะได้ตามรูปแบบเดิม นอกจากนี้ควรตรวจลำดับ error เมื่อ role และ status ผิดพร้อมกันเพื่อคงพฤติกรรม approve เดิม

เอกสารนี้ไม่อ้างว่าได้ implement หรือทดสอบการปฏิเสธแล้ว และไม่ได้แก้ไข source code
