"""Generate the Class 2 slide deck: Test-Driven Development (XML Views, Espresso, TDD)."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---- Theme -------------------------------------------------------------------
NAVY = RGBColor(0x0D, 0x1B, 0x2A)
BLUE = RGBColor(0x1B, 0x4D, 0x7A)
ACCENT = RGBColor(0x3D, 0xDC, 0x84)  # Android green
RED = RGBColor(0xE5, 0x3E, 0x3E)
AMBER = RGBColor(0xF4, 0xB4, 0x00)
LIGHT = RGBColor(0xF2, 0xF4, 0xF7)
GREY = RGBColor(0x5A, 0x6A, 0x7A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CODE_BG = RGBColor(0x1E, 0x1E, 0x2E)
CODE_FG = RGBColor(0xE6, 0xE6, 0xE6)

BODY_FONT = "Calibri"
CODE_FONT = "Consolas"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(BLANK)


def bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def box(slide, l, t, w, h):
    return slide.shapes.add_textbox(l, t, w, h).text_frame


def set_run(run, text, size, color, bold=False, italic=False, font=BODY_FONT):
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font


def accent_bar(slide):
    bar = slide.shapes.add_shape(1, 0, 0, Inches(0.18), SH)
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()


def title_bar(slide, number, title):
    accent_bar(slide)
    tf = box(slide, Inches(0.6), Inches(0.35), Inches(11.8), Inches(1.0))
    r = tf.paragraphs[0].add_run()
    set_run(r, title, 32, NAVY, bold=True)
    chip = slide.shapes.add_shape(1, Inches(12.3), Inches(0.4), Inches(0.7), Inches(0.55))
    chip.fill.solid(); chip.fill.fore_color.rgb = BLUE; chip.line.fill.background()
    ctf = chip.text_frame; ctf.word_wrap = False
    cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
    cr = cp.add_run(); set_run(cr, str(number), 18, WHITE, bold=True)
    ln = slide.shapes.add_shape(1, Inches(0.6), Inches(1.3), Inches(2.4), Inches(0.06))
    ln.fill.solid(); ln.fill.fore_color.rgb = ACCENT; ln.line.fill.background()


def bullets(slide, items, top=Inches(1.7), left=Inches(0.8), width=Inches(11.7),
            height=Inches(5.2), size=20):
    tf = box(slide, left, top, width, height)
    tf.word_wrap = True
    first = True
    for item in items:
        text, level = item if isinstance(item, tuple) else (item, 0)
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = level
        p.space_after = Pt(10)
        bullet = "•  " if level == 0 else "–  "
        r = p.add_run()
        set_run(r, bullet + text, size - level * 2, NAVY if level == 0 else GREY)
    return tf


def speaker(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def shp(slide, kind, l, t, w, h, fill, line=None, line_w=1.0):
    sp = slide.shapes.add_shape(kind, l, t, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is not None:
        sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    else:
        sp.line.fill.background()
    sp.shadow.inherit = False
    return sp


def label(sp, text, size, color, bold=True, sub=None, sub_color=None):
    tf = sp.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); set_run(r, text, size, color, bold=bold)
    if sub:
        p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run(); set_run(r2, sub, size - 8, sub_color or color)


def code_slide(number, title, code, size=14):
    slide = add_slide()
    bg(slide, NAVY)
    accent_bar(slide)
    tf = box(slide, Inches(0.6), Inches(0.3), Inches(12), Inches(0.9))
    r = tf.paragraphs[0].add_run()
    set_run(r, title, 28, WHITE, bold=True)
    chip = slide.shapes.add_shape(1, Inches(12.3), Inches(0.35), Inches(0.7), Inches(0.55))
    chip.fill.solid(); chip.fill.fore_color.rgb = ACCENT; chip.line.fill.background()
    chip.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    set_run(chip.text_frame.paragraphs[0].add_run(), str(number), 18, NAVY, bold=True)
    panel = slide.shapes.add_shape(1, Inches(0.6), Inches(1.35), Inches(12.1), Inches(5.7))
    panel.fill.solid(); panel.fill.fore_color.rgb = CODE_BG
    panel.line.color.rgb = BLUE; panel.line.width = Pt(1)
    ctf = panel.text_frame; ctf.word_wrap = True; ctf.vertical_anchor = MSO_ANCHOR.TOP
    ctf.margin_left = Inches(0.3); ctf.margin_top = Inches(0.2)
    ctf.margin_right = Inches(0.2); ctf.margin_bottom = Inches(0.2)
    for i, line in enumerate(code.split("\n")):
        p = ctf.paragraphs[0] if i == 0 else ctf.add_paragraph()
        p.line_spacing = 1.0
        # colour comments green, RED/GREEN/REFACTOR markers stand out
        color = CODE_FG
        if line.strip().startswith("//"):
            color = RGBColor(0x7E, 0xC6, 0x99)
        set_run(p.add_run(), line if line else " ", size, color, font=CODE_FONT)
    return slide


def table_slide(number, title, headers, rows, col_widths=None, note=None):
    slide = add_slide()
    bg(slide, WHITE)
    title_bar(slide, number, title)
    nrows = len(rows) + 1
    ncols = len(headers)
    gfx = slide.shapes.add_table(nrows, ncols, Inches(0.7), Inches(1.7),
                                 Inches(11.9), Inches(0.6) * nrows)
    table = gfx.table
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = w
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid(); cell.fill.fore_color.rgb = BLUE
        set_run(cell.text_frame.paragraphs[0].add_run(), h, 16, WHITE, bold=True)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.fill.solid(); cell.fill.fore_color.rgb = LIGHT if i % 2 else WHITE
            set_run(cell.text_frame.paragraphs[0].add_run(), val, 13, NAVY)
    if note:
        tf = box(slide, Inches(0.7), Inches(6.7), Inches(11.9), Inches(0.6))
        set_run(tf.paragraphs[0].add_run(), note, 14, GREY, italic=True)
    return slide


def tdd_cycle(slide, top=Inches(2.2)):
    """Red -> Green -> Refactor loop."""
    boxes = [("RED", "write a failing test", RED, WHITE),
             ("GREEN", "simplest code to pass", ACCENT, NAVY),
             ("REFACTOR", "clean up, stay green", BLUE, WHITE)]
    x = Inches(1.2); w = Inches(3.2); gap = Inches(0.75); h = Inches(1.8)
    for i, (t, sub, c, tc) in enumerate(boxes):
        b = shp(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, top, w, h, c)
        label(b, t, 26, tc, sub=sub, sub_color=tc)
        if i < 2:
            shp(slide, MSO_SHAPE.RIGHT_ARROW,
                Emu(int(x) + int(w) + int(Inches(0.06))),
                Emu(int(top) + int(Inches(0.65))),
                Emu(int(gap) - int(Inches(0.12))), Inches(0.5), GREY)
        x = Emu(int(x) + int(w) + int(gap))
    cap = box(slide, Inches(1.0), Emu(int(top) + int(h) + int(Inches(0.55))), Inches(11.4), Inches(0.7))
    cp = cap.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
    set_run(cp.add_run(),
            "↺  repeat  —  never write production code without a failing test first",
            18, GREY, italic=True)


def espresso_flow(slide, top=Inches(4.9)):
    steps = [("onView", "matcher", BLUE), ("perform", "action", ACCENT), ("check", "assertion", NAVY)]
    x = Inches(1.3); w = Inches(3.2); h = Inches(1.2)
    for t, sub, c in steps:
        b = shp(slide, MSO_SHAPE.CHEVRON, x, top, w, h, c)
        tc = NAVY if c == ACCENT else WHITE
        label(b, t, 20, tc, sub=sub, sub_color=tc)
        x = Emu(int(x) + int(w) - int(Inches(0.35)))


# ============================================================================
# Slide 1 — Title
# ============================================================================
s = add_slide(); bg(s, NAVY)
blk = s.shapes.add_shape(1, 0, Inches(2.7), SW, Inches(0.12))
blk.fill.solid(); blk.fill.fore_color.rgb = ACCENT; blk.line.fill.background()
tf = box(s, Inches(1.0), Inches(1.5), Inches(11.3), Inches(1.4))
set_run(tf.paragraphs[0].add_run(), "Test-Driven Development", 52, WHITE, bold=True)
tf2 = box(s, Inches(1.0), Inches(2.9), Inches(11.3), Inches(0.9))
set_run(tf2.paragraphs[0].add_run(), "Class 2 — Red · Green · Refactor", 26, ACCENT, bold=True)
tf3 = box(s, Inches(1.0), Inches(4.0), Inches(11.3), Inches(1.2))
set_run(tf3.paragraphs[0].add_run(),
        "XML Views  ·  Espresso  ·  Espresso-Intents  ·  a Shopping Cart kata", 20, LIGHT)
speaker(s, "Last session we tested logic and UI concepts. Today we flip the order: tests first, "
           "then code. We close the pending item — testing an XML View with Espresso — and then "
           "build a Shopping Cart with strict TDD.")

# ============================================================================
# Slide 2 — Where we are (roadmap)
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 2, "Where we are")
bullets(s, [
    ("1.  Unit, integration and UI tests", 0),
    ("2.  TDD  ◀  today", 0),
    ("3.  Mocks, stubs and fakes", 0),
    ("4.  UI testing and CI/CD", 0),
    ("5.  Fixing flaky tests", 0),
    ("6.  Catching bugs, plus the exam", 0),
])
speaker(s, "We have logic tested (LoginValidator). We do NOT have the view tested. "
           "That is today's first goal, and TDD is the method for everything after.")

# ============================================================================
# Slide 3 — Today's agenda
# ============================================================================
table_slide(3, "Today's agenda",
            ["#", "Topic", "Type", "Est."],
            [
                ["1", "Creating an XML Login View", "Live coding", "20 min"],
                ["2", "Navigation on successful login", "Live coding", "15 min"],
                ["3", "Testing the View with Espresso", "Live coding + lab", "30 min"],
                ["4", "The Shop screen (items list)", "Live coding", "20 min"],
                ["5", "Checkout — Shopping Cart via TDD", "Lab (red/green/refactor)", "45 min"],
            ],
            col_widths=[Inches(0.8), Inches(5.6), Inches(3.5), Inches(2.0)])

# ============================================================================
# Slide 4 — Recap: logic tested, view not
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 4, "Recap — and the gap")
bullets(s, [
    "Class 1: we unit-tested pure logic (LoginValidator)",
    "The rules are proven — but nothing tests the actual screen",
    "Pending item: test an XML View with Espresso",
    "Plan: put a UI on tested logic, then drive new logic with TDD",
])
speaker(s, 'Talking point: "We have logic tested. We do NOT have the view tested. '
           'That is today\'s first goal."')

# ============================================================================
# Slide 5 — What is TDD?
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 5, "What is TDD?")
bullets(s, [
    "Test-Driven Development: write the test before the code",
    "The test describes the behaviour you want next",
    "You only write enough code to make it pass",
    "Design emerges from the tests, not the other way around",
    "A test you never watched fail proves nothing",
])

# ============================================================================
# Slide 6 — The TDD cycle (diagram)
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 6, "The TDD cycle")
tdd_cycle(s)
speaker(s, "Red: write a failing test that fails for the RIGHT reason. Green: the simplest "
           "code that passes, even if it looks like cheating. Refactor: clean up while tests "
           "stay green. Then repeat.")

# ============================================================================
# Slide 7 — Uncle Bob's three rules
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 7, "The three rules of TDD")
bullets(s, [
    "1.  No production code until you have a failing test",
    "2.  No more of a test than is sufficient to fail",
    "3.  No more production code than is sufficient to pass",
    "In a compiled language, a compile error IS a failing test",
], size=22)
speaker(s, "These are Robert C. Martin's three laws. Rule 3 is the hard one for students — "
           "they want to write the whole class at once.")

# ============================================================================
# Slide 8 — RED
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 8, "RED — write a failing test")
bullets(s, [
    "Express one small piece of behaviour as a test",
    "Run it and watch it fail — confirm it fails for the right reason",
    "A missing class or method that won't compile counts as red",
    "This is where you discover what the API should look like",
])
shp(s, MSO_SHAPE.OVAL, Inches(11.0), Inches(1.9), Inches(1.2), Inches(1.2), RED)

# ============================================================================
# Slide 9 — GREEN
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 9, "GREEN — make it pass")
bullets(s, [
    "Write the simplest code that turns the test green",
    'Hardcoding a return value is allowed — even "cheating"',
    "Do not add behaviour the tests don't yet demand",
    "Green means safe: you now have a checkpoint",
])
shp(s, MSO_SHAPE.OVAL, Inches(11.0), Inches(1.9), Inches(1.2), Inches(1.2), ACCENT)

# ============================================================================
# Slide 10 — REFACTOR
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 10, "REFACTOR — clean up")
bullets(s, [
    "Improve the code now that behaviour is locked in by tests",
    "Remove duplication, name things, extract constants",
    "Run the tests after every change — they must stay green",
    "Fearless refactoring is the payoff of TDD",
])
shp(s, MSO_SHAPE.OVAL, Inches(11.0), Inches(1.9), Inches(1.2), Inches(1.2), BLUE)

# ============================================================================
# Slide 11 — TDD drives requirements
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 11, "TDD forces the requirements talk")
bullets(s, [
    'Before any code, resolve the ambiguity in "apply a discount":',
    ('"Greater than 200" — is exactly 200 discounted?  →  No, strictly greater', 1),
    ("Tiered or single bracket?  →  single: >300 → 20%, else >200 → 10%, else 0%", 1),
    ("Remove an item that isn't there?  →  no-op", 1),
    ("Duplicate items allowed?  →  yes", 1),
    "The real value of TDD: the conversation happens before the code exists",
])
speaker(s, "TDD forces you to pin down behaviour up front. Every answer above becomes a test.")

# ============================================================================
# Slide 12 — Keep Activities dumb (bridge to UI)
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 12, "Keep the Activity dumb")
bullets(s, [
    "The Activity's only job: read input → ask the validator → show error or navigate",
    "No business logic in the Activity — it lives in tested classes",
    "That is exactly what we assert with Espresso",
    "Thin UI + tested logic = easy to test both layers",
])
espresso_flow(s, top=Inches(5.1))

# ============================================================================
# Slide 13 — Espresso mental model
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 13, "The Espresso mental model")
bullets(s, [
    "onView( matcher )  →  find the view",
    "      .perform( action )  →  do something to it",
    "      .check( assertion )  →  verify something about it",
    "Espresso synchronises with the UI thread automatically",
    "So you never write Thread.sleep() — ever",
], size=21)

# ============================================================================
# Slide 14 — Espresso cheat sheet
# ============================================================================
table_slide(14, "Espresso for Views — cheat sheet",
            ["Matchers", "Actions", "Assertions"],
            [
                ["withId()", "click()", "matches(isDisplayed())"],
                ["withText()", "typeText()", "matches(withText(...))"],
                ["withHint()", "replaceText()", "doesNotExist()"],
                ["isDisplayed()", "closeSoftKeyboard()", "matches(isEnabled())"],
                ["isEnabled()", "scrollTo()", "— custom matchers —"],
            ],
            col_widths=[Inches(3.9), Inches(4.0), Inches(4.0)],
            note="Turn OFF device animations — Espresso's idling breaks with animations on.")

# ============================================================================
# Slide 15 — Two teaching rules
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 15, "Two rules that make Views testable")
bullets(s, [
    "Every testable widget needs an android:id",
    ("withId() is Espresso's primary matcher — no id, no test", 1),
    "TextInputLayout owns the error; TextInputEditText owns the text",
    ("Assert errors on tilEmail, type text into inputEmail", 1),
    "Keep Activities dumb — push logic into testable classes",
])

# ============================================================================
# Slide 16 — Testing navigation with Espresso-Intents
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 16, "Testing navigation")
bullets(s, [
    "On valid login the Activity fires an Intent to the next screen",
    "We care about the observable outcome: an Intent was sent",
    "Espresso-Intents asserts it without launching the second screen",
    ("Intents.intended(hasComponent(ShopActivity::class.java.name))", 1),
    ("Intents.assertNoUnverifiedIntents() — proves it did NOT navigate", 1),
    "Wrap tests with Intents.init() / Intents.release()",
])

# ============================================================================
# Slide 17 — Custom matcher (code)
# ============================================================================
code_slide(17, "A custom matcher for TextInputLayout errors", '''// Espresso has no built-in error matcher for TextInputLayout — write one.
fun hasTextInputLayoutError(expected: String): Matcher<View> =
    object : TypeSafeMatcher<View>() {

        override fun describeTo(description: Description) {
            description.appendText("TextInputLayout with error: $expected")
        }

        override fun matchesSafely(view: View): Boolean {
            if (view !is TextInputLayout) return false
            return view.error?.toString() == expected
        }
    }

// Use it like any other assertion:
onView(withId(R.id.tilEmail))
    .check(matches(hasTextInputLayoutError("Email is required")))''')

# ============================================================================
# Slide 18 — Shopping Cart kata (requirements)
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 18, "The Shopping Cart kata")
bullets(s, [
    "1.  New cart → subtotal is 0",
    "2.  Add items to the cart",
    "3.  Remove items from the cart",
    "4.  Subtotal = sum of item prices, then apply a discount:",
    ("10% if subtotal > 200", 1),
    ("20% if subtotal > 300", 1),
    "We build this class test-first, one behaviour at a time",
])

# ============================================================================
# Slide 19 — Boundaries
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 19, "Test the boundaries")
bullets(s, [
    "Bugs live at the edges: 200 and 300",
    "exactly 200 → no discount   (strictly greater)",
    "just over 200 (250) → 10%",
    "exactly 300 → still 10%",
    "over 300 (400) → 20%",
    "> vs >= is the most common off-by-one in business rules",
])
shp(s, MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(10.6), Inches(2.1), Inches(2.2), Inches(2.0), AMBER)

# ============================================================================
# Slide 20 — TDD walkthrough (code)
# ============================================================================
code_slide(20, "Red → Green, in small steps", '''// RED: the first test doesn't even compile — that's our first failure
@Test fun `empty cart subtotal is zero`() {
    assertEquals(0.0, ShoppingCart().subtotal(), 0.001)
}
fun subtotal(): Double = 0.0                 // GREEN (hardcoded, on purpose)

// RED: subtotal must add prices
@Test fun `subtotal adds up all item prices`() {  /* 80 + 45 = 125 */ }
fun subtotal(): Double = items.sumOf { it.price } // GREEN (0.0 test still passes)

// RED: the discount boundaries, then GREEN:
private fun discountRate(raw: Double): Double = when {
    raw > 300 -> 0.20
    raw > 200 -> 0.10
    else      -> 0.0
}''')

# ============================================================================
# Slide 21 — Regression safety
# ============================================================================
s = add_slide(); bg(s, WHITE); title_bar(s, 21, "Regression safety, live")
bullets(s, [
    "Replacing the hardcoded 0.0 with a real sum keeps the empty-cart test green",
    "sumOf on an empty list is 0.0 — the old behaviour is preserved",
    "Extracting constants (TIER_1_RATE, thresholds) changes nothing observable",
    "Run all tests after each refactor → still green",
    "That safety net is why TDD lets you refactor without fear",
])

# ============================================================================
# Slide 22 — Which test at which layer
# ============================================================================
table_slide(22, "Which test proves what",
            ["Layer", "Tool", "Speed", "What it proves"],
            [
                ["Pure logic (ShoppingCart, LoginValidator)", "JUnit", "ms", "The rules are right"],
                ["View, on the JVM", "Robolectric + Espresso", "~1 s", "The screen wires up"],
                ["View, on a device", "Espresso instrumented", "~10 s", "It really works"],
            ],
            col_widths=[Inches(4.8), Inches(3.3), Inches(1.3), Inches(2.5)])

# ============================================================================
# Slide 23 — Summary & homework
# ============================================================================
s = add_slide(); bg(s, NAVY); accent_bar(s)
tf = box(s, Inches(0.6), Inches(0.4), Inches(12), Inches(1.0))
set_run(tf.paragraphs[0].add_run(), "Summary & homework", 32, WHITE, bold=True)
ln = s.shapes.add_shape(1, Inches(0.65), Inches(1.35), Inches(2.4), Inches(0.06))
ln.fill.solid(); ln.fill.fore_color.rgb = ACCENT; ln.line.fill.background()
tf = box(s, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0)); tf.word_wrap = True
items = [
    ("Give every widget an id — it's your test API", False),
    ("Keep Activities dumb; push logic into testable classes", False),
    ("Test boundaries (200 and 300), not just happy paths", False),
    ("RED → GREEN → REFACTOR — never skip red", False),
    ("Homework: add quantity support with TDD (commit the red test separately)", True),
    ("Homework: Espresso test that the cart resets after checkout", True),
]
for i, (t, hw) in enumerate(items):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.space_after = Pt(12)
    set_run(p.add_run(), "•  " + t, 21, ACCENT if hw else LIGHT, bold=hw)

prs.save("slides/Class2_TDD.pptx")
print("Saved slides/Class2_TDD.pptx with", len(prs.slides._sldIdLst), "slides")
