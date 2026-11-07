# Panda Suite

ดู [คู่มือใช้ครบทุก skill](docs/usage.md) สำหรับวิธีเรียกใช้ สิ่งที่ต้องเตรียม
ตัวอย่าง prompt ผลลัพธ์ที่คาดหวัง และขอบเขตสิทธิ์ของทั้ง 16 skills

ชุด Agent Skills สำหรับงานวิศวกรรมซอฟต์แวร์และการส่งมอบผลิตภัณฑ์ โดยมี
**Panda Lead** ช่วยเลือก workflow เท่าที่จำเป็น แต่ละ skill เรียกใช้แยกกันได้
ไม่มี server, database หรือระบบ multi-agent ที่จำเป็นต้องติดตั้งเพิ่ม

[English guide](README.md) · [สถาปัตยกรรม](docs/architecture.md) ·
[ผลตรวจสอบและข้อจำกัด](docs/verification.md)

## เลือก skill ให้ตรงงาน

| Skill | หน้าที่ |
| --- | --- |
| `panda-lead` | เลือกและประสาน workflow ตามเป้าหมายและสิทธิ์ที่ได้รับ |
| `panda-brainstorm` | สำรวจปัญหา สมมติฐาน ทางเลือก และ trade-off |
| `panda-plan` | วางงานตามลำดับ พร้อม acceptance criteria และวิธีตรวจสอบ |
| `panda-execute` | ลงมือทำงานที่ได้รับอนุญาตและรายงานผลจริง |
| `panda-debugger` | วิเคราะห์สาเหตุจากหลักฐาน ใช้ skill ต้นฉบับ |
| `panda-review` | ตรวจข้อผิดพลาดสำคัญใน diff |
| `panda-simplify` | ลดความซับซ้อนโดยรักษาพฤติกรรมและข้อกำหนดสำคัญ |
| `buddhist-method` | ใช้วินัยการคิดเมื่อต้องตรวจข้อเท็จจริง ตัดสินใจ หรือรับมือความไม่แน่นอน |
| `panda-write` | เขียนเอกสารโครงการและคู่มือนักพัฒนา |
| `panda-spec` | เขียน technical specification ภาษาไทยหรืออังกฤษ |
| `panda-manual` | เขียนคู่มือผู้ใช้จากพฤติกรรม UI ที่สังเกตได้หรือหลักฐานที่ให้มา |

คำถามอธิบาย function ไม่ควรสร้างแผนโครงการ การระดมความคิดไม่ใช่การอนุญาต
ให้แก้โค้ด และไม่ต้องโหลด Buddhist Method ในทุกขั้นตอน

## ติดตั้งจาก checkout นี้

เลือกวิธีเดียวเพื่อหลีกเลี่ยง skill ชื่อซ้ำ ใช้ branch `codex/panda-suite` ตามคำสั่ง clone ในคู่มือภาษาอังกฤษ
คำสั่งติดตั้งด้านล่างให้รันจาก checkout ในเครื่อง

Claude Code แบบไม่ติดตั้งถาวร:

```sh
claude --plugin-dir "$PWD"
```

จากนั้นใช้ `/panda-suite:panda-lead` หรือ `/panda-suite:panda-spec`

Codex แบบ local marketplace:

```sh
codex plugin marketplace add "$PWD"
codex plugin add panda-suite@panda-suite
```

เลือก skill จาก selector ของ host โดย inventory ที่ตรวจพบใช้ชื่อ
`panda-suite:panda-lead` การอ่านแพ็กเกจและ discovery ผ่านแล้ว แต่ยังไม่ได้ทดสอบ
การติดตั้งถาวรและการเรียกโมเดลผ่าน plugin ใน session แบบ interactive

ติดตั้งเฉพาะ skill สำหรับ Codex ในโครงการอื่น:

```sh
python3 scripts/install-skills.py --destination /path/to/project/.agents/skills --skill panda-spec
```

หรือใช้ `--all` เพื่อติดตั้งทั้งชุด ต้องมี Python 3.10 ขึ้นไป ตัวติดตั้งจะปฏิเสธ
ชื่อที่มีอยู่แล้วและไม่เขียนทับ skill เดิม หากเกิด I/O error ระหว่างคัดลอก
ให้ตรวจ directory ที่สร้างใหม่ก่อนลองอีกครั้ง

Standalone Codex ใช้ `$panda-spec`; Claude Code ที่ติดตั้งไว้ใน
`$HOME/.claude/skills` ใช้ `/panda-spec` รายละเอียดการติดตั้งทุกแบบอยู่ใน
[คู่มือภาษาอังกฤษ](README.md)

## ตัวอย่าง

```text
$panda-lead อธิบาย function นี้โดยอ้างอิง source code

$panda-plan วางแผนเพิ่ม rejection flow สำหรับ manager จาก requirements.md
ระบุ acceptance criteria และวิธีทดสอบ ยังไม่ต้องแก้โค้ด

$panda-debugger วิเคราะห์ว่าทำไม transfer สำเร็จแต่ยอดเงินไม่เปลี่ยน
แสดงหลักฐานและระดับความมั่นใจ ห้ามแก้โค้ด

$panda-spec เขียน Backend Technical Specification ภาษาไทย
แยกพฤติกรรมปัจจุบัน ข้อเสนอ และประเด็นที่ยังต้องตัดสินใจ
```

งานที่ขอให้ implement อย่างชัดเจนถือว่าอนุญาตให้แก้ไฟล์ที่เกี่ยวข้องแล้ว
ไม่ถามอนุมัติซ้ำโดยไม่มีเหตุผล แต่การเปลี่ยน scope สำคัญ การลบข้อมูล
การแก้ production การ deploy การ publish และผลกระทบต่อระบบภายนอก
ต้องมีสิทธิ์ครอบคลุมการกระทำนั้น

คู่มือ UI ต้องแยกสิ่งที่สังเกตจริงจากข้อมูลในเอกสาร หากไม่มี browser ให้ส่ง
draft ที่ระบุข้อจำกัด ห้ามสร้าง screenshot หรือผลทดสอบขึ้นเอง

## ตรวจสอบ

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate-skills.py
python3 scripts/vendor-upstreams.py
.venv/bin/python -m unittest discover -s tests -p 'test_tooling.py' -v
```

มี scenario สำหรับทุก skill พร้อม fixtures และผลการทดลองจริงใน
[evaluation guide](tests/evaluation.md) และ [ผลประเมิน](tests/results/2026-11-07/summary.md)
ผลเดิมมีข้อผิดพลาดด้าน Unicode แม้ผ่าน test ที่ให้มาครบ จึงไม่ได้อ้างว่า
ชุด skill ทำให้แม่นยำกว่า baseline หรือประหยัด token โดยไม่มีหลักฐาน

## ที่มาและ license

ใช้ไฟล์ต้นฉบับจาก [Panda Debugger](https://github.com/akkaraponph/panda-debugger)
และ [Buddhist Method](https://github.com/akkaraponph/buddhist-method)
โดยเก็บ revision และ SHA-256 ใน `upstream-lock.json`

ไฟล์ที่เขียนใหม่ของ Suite ใช้ MIT ส่วน Buddhist Method เก็บ MIT เดิมไว้
revision ของ Panda Debugger ที่ตรวจสอบไม่มีไฟล์ LICENSE จึงยังไม่มีข้อสรุป
สิทธิ์สำหรับเผยแพร่ไฟล์ส่วนนั้นต่อ และไม่อยู่ใน MIT ของ Suite
ดู [รายละเอียด attribution และ license](SOURCE_NOTICES.md)

## ส่วนขยายที่จำเป็น

เพิ่ม `panda-requirements`, `panda-test`, `panda-impact`, `panda-release` และ `panda-skill-lab` พร้อม routing ใน Panda Lead รวมเป็น 16 skills โดย Panda Debugger และ Buddhist Method เป็น skill หลัก และเก็บเอกสารเทคนิคใน `references/` ของแต่ละ skill ดู [รายงานส่วนขยาย](docs/expansion.md) ไม่มีการ commit หรือ deploy
