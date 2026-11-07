# Buddhist Method — skill สำหรับ Claude

Skill ที่นำหลักธรรมในพระพุทธศาสนา 6 ข้อ มาใช้เป็นวินัยการทำงานของ Claude (หรือ LLM อื่นๆ) แต่ละหลักจับ failure mode ที่ LLM พังบ่อย: เชื่อ pattern แทนที่จะ verify, แก้อาการแทนที่จะแก้เหตุ, ยอมตามแรงกดดันแทนที่จะดูหลักฐาน

> 🇬🇧 Read [README.md](README.md) for the English version

## ทำไมต้องใช้ skill นี้

ความผิดพลาดส่วนใหญ่ของ LLM ในงานจริงไม่ใช่ช่องว่างของความรู้ แต่เป็นช่องว่างของวินัย — โมเดลรู้วิธีเช็ค flag, หา root cause, หรือรันเทสต์ซ้ำอยู่แล้ว แต่พอเจอแรงกดดันด้านเวลา, user ที่มั่นใจมากๆ, หรืองานยาวหลายขั้น มันจะข้ามขั้นตอนนั้น สั่งว่า "ระวังหน่อย" ก็ไม่ช่วย เพราะ "ระวัง" ไม่มี trigger — ไม่มีอะไรบอกโมเดลว่าต้องระวัง*เรื่องไหน* *เมื่อไร*

skill นี้แปลงวินัยที่ขาดหายให้เป็น checklist ที่มีชื่อ แต่ละหลักประกอบด้วย **trigger** (สถานการณ์รูปธรรมที่สังเกตได้) + **action** (สิ่งที่ควรทำแทน reflex) + **anti-pattern** (หน้าตาของความพัง) คุณสมบัติสองข้อที่สำคัญในทางปฏิบัติ:

- **มันทำงานที่จุดตัดสินใจ ไม่ใช่แบบลอยๆ** — "กำลังจะพูดข้อเท็จจริงจากความจำ" หรือ "กำลังจะครอบ try/catch บน error ที่ยังไม่เข้าใจ" คือ*ช่วงเวลา* ไม่ใช่อารมณ์ checklist ที่ผูกกับช่วงเวลาถึงจะถูกใช้จริง
- **มันถูก** — skill โหลด on demand และ core มีไฟล์เดียว ใช้ไม่กี่ร้อย token ในจังหวะที่ถูกต้อง แทนคำเทศน์ยาวๆ ที่แปะอยู่ทุก prompt

เวอร์ชันปัจจุบันผ่าน pressure test มาแล้ว: agent ที่ทำงานภายใต้วิธีนี้ตรวจสอบ diagnosis ผิดๆ ที่ถูกยืนยันมาอย่างมั่นใจก่อนส่งงานครบ 7/7 run และไม่มีการอ้างว่า "tests pass" โดยไม่ได้รันจริงเลยทั้ง 7 run — รวมถึงกรณี test suite ที่กินเวลา 2.5 นาทีพร้อมเพื่อนร่วมทีมเร่งให้เร็ว ดูวิธีการ ผลลัพธ์ และข้อจำกัดได้ที่ [tests/pressure-baseline.md](tests/pressure-baseline.md)

## มีอะไรในนี้

Skill (`SKILL.md` + `references/`) ที่ให้ Claude ใช้เป็น checklist:

| หลัก | จับ failure mode |
|------|------------------|
| **กาลามสูตร** (Kalāma) | พูดข้อเท็จจริงจากความจำ training data โดยไม่ verify |
| **โยนิโสมนสิการ** (Yoniso) | แก้ที่อาการ ไม่ใช่ที่เหตุ |
| **สติ-สัมปชัญญะ** (Sati-Sampajañña) | ทำต่อจาก state ที่จำได้ ทั้งที่ของจริงเปลี่ยนแล้ว |
| **อนัตตา** (Anatta) | ติด draft แรก ไม่ยอมเขียนใหม่ |
| **ปหานะ** (Pahāna) | workaround ที่ซ่อนบั๊ก แทนที่จะตัดเหตุ |
| **อุเบกขา** (Upekkhā) | ยอมตาม user เมื่อโดน push หรือลนลานเมื่อเครื่องมือ fail |

พร้อม reference สำหรับสถานการณ์ยากกว่า:
- **อริยสัจ 4** เป็นกรอบ debug (`references/ariyasacca-debug.md`)
- **อปายโกศล** — รู้ว่ากำลังเสื่อม / anti sunk-cost
- **อัปปมาทะ** — ความไม่ประมาทในงานยาว
- **อิทธิบาท 4** — ฐานสี่ที่พางานสำเร็จ (ฉันทะ / วิริยะ / จิตตะ / วิมังสา)
- **กุสลธัมมฉันทะ** — อยากได้งานที่ครบถ้วน: ไม่ทิ้ง placeholder / stub ในงานที่ส่งมอบ
- **สัปปุริสธรรม 3 ใน 7** — รู้ตน / รู้กาล / รู้บริษัท
- **อัตถะ 2 ระดับ** — ทิฏฐธัมมิกัตถะ vs สัมปรายิกัตถะ (ประโยชน์ปัจจุบัน vs อนาคต)
- **มัชฌิมาปฏิปทา** — ทางสายกลางในการ sizing solution
- **อนาคตังสญาณ** — มองอนาคตแบบจำกัดขอบเขต 1 ก้าว กันโค้ดวันนี้บังคับ refactor วันหน้า
- **ปริญญา** — วินิจฉัยให้ขาดก่อนแก้: เขียนสาเหตุออกมาก่อนลงมือ ไม่เดามั่วเป็นวงจร
- **พรหมวิหาร** — ปรับโทน/น้ำเสียงของคำตอบให้เข้ากับสภาวะอารมณ์ของผู้ใช้

## ทำไมเก็บชื่อบาลี/ไทย ไว้

ชื่อบาลีไม่ได้เก็บไว้เพื่อตกแต่ง แต่เป็น mnemonic — ชื่อสั้นที่ดึง pattern ครบทั้งชุดออกมาในทีเดียว "โยนิโสมนสิการ" ดึงวินัยทั้งหมดเรื่องการตั้งจิตไปหาเหตุ ขณะที่ "root cause analysis" ดึงไม่หมด

เหมือนวิศวกรเรียก "sigmoid" ไม่เรียก "ฟังก์ชันโค้งๆ" — ชื่อคือ infrastructure

skill นี้**ไม่ใช่**กรอบศาสนา ไม่ต้องเชื่อ ไม่ต้องปฏิบัติธรรมเพื่อใช้ มันคือ checklist ที่มีรากทางวัฒนธรรม นำเสนออย่างตรงไปตรงมา ถ้าอยากศึกษาหลักธรรมในความลึกจริงๆ อ่านพระไตรปิฎก — skill นี้ไม่ได้อ้างจะสอน

## วิธีใช้

### กับ Claude Code

Paste prompt นี้ลง Claude Code — clone skill และ wiring `~/.claude/CLAUDE.md` ครั้งเดียวจบ:

```
Install the buddhist-method skill:
1. Run: git clone https://github.com/nai0om/buddhist-method ~/.claude/skills/buddhist-method
2. Open ~/.claude/CLAUDE.md (create it if it does not exist) and append:

## Working method
For tasks involving factual claims, debugging, user pushback,
or long multi-step work, consult the buddhist-method skill at
~/.claude/skills/buddhist-method/SKILL.md before responding.
```

หลังจากนั้น Claude Code จะ reference skill นี้โดยอัตโนมัติทุก session

### กับ Claude product อื่น

ที่ไหนรองรับ skill ก็วางไฟล์ลงได้เลย โครงสร้างมาตรฐาน (`SKILL.md` มี YAML frontmatter + `references/`)

### ใช้เป็น reference เฉยๆ ก็ได้

`SKILL.md` กับ `references/` อ่านเดี่ยวๆ ได้ ไม่ต้องมี Claude แต่ละหลักมี **trigger** (ใช้เมื่อไร) กับ **action** (ทำอะไร) ใช้เป็น checklist ส่วนตัวก็ได้

### ทำให้ active ตลอด (ทางเลือก)

ปกติ Claude จะโหลด skill on-demand — เห็น description แล้วตัดสินใจเองว่าจะอ่าน `SKILL.md` เต็มๆ ไหม ขึ้นกับงานตรงหน้า แบบนี้พอสำหรับการใช้งานทั่วไป และเก็บ context budget ไว้ใช้กับเรื่องอื่น

ถ้าอยากให้ skill active ตลอดไม่ว่าทำงานอะไร เพิ่ม pointer สั้นๆ ลงใน `CLAUDE.md`:

```markdown
## Working method
For tasks involving factual claims, debugging, user pushback,
or long multi-step work, consult the buddhist-method skill at
~/.claude/skills/buddhist-method/SKILL.md before responding.
```

ใส่ได้สองที่:

- **`CLAUDE.md` ใน project root** — ทำงานเฉพาะใน project นั้น
- **`~/.claude/CLAUDE.md`** — ทำงานทุก project ของ Claude Code

Pointer สั้นแค่ไม่กี่บรรทัด ไม่กิน context มาก Claude ยังโหลด body ของ skill ตอน trigger ติดเหมือนเดิม — แค่การันตีว่า skill อยู่ในสายตา Claude เสมอ

## โครงสร้าง

```
buddhist-method/
├── SKILL.md                              # 6 หลัก core + dispatch
├── README.md                             # เวอร์ชันอังกฤษ
├── README.th.md                          # ไฟล์นี้
├── LICENSE                               # MIT
├── references/
│   ├── ariyasacca-debug.md               # อริยสัจ 4 เป็นกรอบ debug
│   └── extended-principles.md            # 10 หลักรอง
└── tests/
    └── pressure-baseline.md              # บันทึกผล pressure test (RED baseline)
```

## License

MIT — ใช้ แก้ไข แจกต่อได้เสรี ดู [LICENSE](LICENSE)

## ร่วมพัฒนา

เปิดรับ issue และ pull request โดยเฉพาะ:
- failure mode ที่ 6 หลักปัจจุบันยังจับไม่ได้
- trigger ที่ดีกว่า (สถานการณ์เฉพาะที่ควรกระตุ้นแต่ละหลัก)
- การแปลเป็นภาษาอื่นที่รากของหลักธรรมยังมีชีวิตอยู่

ถ้าจะเสนอหลักใหม่ ขอให้แสดง:
1. failure mode เฉพาะที่หลักนั้นจับ
2. trigger กับ action ที่เป็นรูปธรรม
3. ทำไมหลักที่มีอยู่ยังจับไม่ได้

มาตรฐานของ skill นี้คือ**ความกระชับ** — เพิ่มหลักง่าย แต่ที่ยากคือรักษาจำนวนให้น้อยพอที่จะใช้จริง

ดู [tests/pressure-baseline.md](tests/pressure-baseline.md) เป็นตัวอย่างหลักฐานที่ใช้ได้ — บันทึก pressure test ที่รันกับ skill เวอร์ชันปัจจุบัน รวมถึง failure mode หนึ่งที่สังเกตเห็นแล้วแต่ยังไม่ได้บัญญัติ (การคุมขอบเขตงาน)
