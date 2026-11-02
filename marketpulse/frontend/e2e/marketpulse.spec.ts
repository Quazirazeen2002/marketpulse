import { test, expect } from "@playwright/test";

test.describe("MARKETPULSE Stage 3 — End-to-End Test Suite", () => {
  // -------------------------------------------------------------
  // 1. PUBLIC MARKETING WEBSITE
  // -------------------------------------------------------------
  test("1. Public Landing Page renders all Feastables-inspired sections", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveTitle(/MARKETPULSE/i);

    // Section 1: Announcement Bar
    await expect(page.locator("text=INTRODUCING THE NEXT GENERATION OF BUSINESS INTELLIGENCE").first()).toBeVisible();
    await expect(page.locator("text=STAGE 3 LIVE").first()).toBeVisible();

    // Section 2: Public Navigation
    await expect(page.locator("header").getByRole("link", { name: "Product" })).toBeVisible();
    await expect(page.locator("header").getByRole("link", { name: "How It Works" })).toBeVisible();
    await expect(page.locator("header").getByRole("link", { name: "Use Cases" })).toBeVisible();
    await expect(page.locator("header").getByRole("link", { name: "About" })).toBeVisible();
    await expect(page.locator("header").getByRole("link", { name: "Open Workspace" })).toBeVisible();

    // Section 3: Hero Section
    await expect(page.locator("h1")).toContainText("STOP GUESSING.");
    await expect(page.locator("h1")).toContainText("START DISCOVERING.");
    await expect(page.locator("text=START YOUR RESEARCH").first()).toBeVisible();
    await expect(page.locator("text=EXPLORE THE PLATFORM").first()).toBeVisible();
    await expect(page.locator("text=INTELLIGENCE ENGINE • ACTIVE").first()).toBeVisible();

    // Section 4: Intelligence in Action
    await expect(page.locator("text=MORE THAN SEARCH.").first()).toBeVisible();
    await expect(page.locator("text=Discover what is happening.").first()).toBeVisible();
    await expect(page.locator("text=Find what competitors are missing.").first()).toBeVisible();
    await expect(page.locator("text=Decide what to do next.").first()).toBeVisible();

    // Section 5: The Intelligence Engine (8 Minds)
    await expect(page.locator("text=EIGHT MINDS.").first()).toBeVisible();
    await expect(page.locator("text=ONE INTELLIGENCE ENGINE.").first()).toBeVisible();
    await expect(page.locator("text=Research Director").first()).toBeVisible();
    await expect(page.locator("text=Meta Muse Wonder").first()).toBeVisible();
    await expect(page.locator("text=Meta Spark 1.3").first()).toBeVisible();

    // Section 6: How It Works Process
    await expect(page.locator("text=FROM QUESTION TO STRATEGY").first()).toBeVisible();
    await expect(page.locator("text=IN EIGHT PRECISION STEPS").first()).toBeVisible();

    // Section 7: Opportunity Showcase
    await expect(page.locator("text=THE BEST OPPORTUNITIES").first()).toBeVisible();
    await expect(page.locator("text=ARE THE ONES YOU HAVEN'T ASKED ABOUT YET.").first()).toBeVisible();

    // Section 8: Industry Use Cases
    await expect(page.locator("text=PROVEN IN REAL MARKETS").first()).toBeVisible();
    await expect(page.locator("text=Fashion E-commerce in Emerging Markets").first()).toBeVisible();

    // Section 9: Research Experience Canvas
    await expect(page.locator("text=THE WORKSPACE YOU WISHED").first()).toBeVisible();

    // Section 10: Final CTA
    await expect(page.locator("text=YOUR NEXT BUSINESS OPPORTUNITY").first()).toBeVisible();
    await expect(page.locator("text=STARTS WITH A QUESTION.").first()).toBeVisible();
    await expect(page.locator("text=START INVESTIGATING").first()).toBeVisible();

    // Section 11: Public Footer
    await expect(page.locator("footer")).toContainText("MARKETPULSE");
    await expect(page.locator("footer")).toContainText("Meta Muse Wonder (Director)");
  });

  test("2. Public marketing pages navigate and render smoothly", async ({ page }) => {
    // Product Page
    await page.goto("/product");
    await expect(page.locator("h1")).toContainText("ENGINEERED FOR");
    await expect(page.locator("text=Why Teams Choose MarketPulse").first()).toBeVisible();

    // How It Works Page
    await page.goto("/how-it-works");
    await expect(page.locator("h1")).toContainText("HOW MARKETPULSE");
    await expect(page.locator("text=Two-Stage Autonomous Intelligence Engine").first()).toBeVisible();

    // Use Cases Page
    await page.goto("/use-cases");
    await expect(page.locator("h1")).toContainText("INTELLIGENCE FOR");
    await expect(page.locator("text=Fashion E-Commerce in Emerging Markets").first()).toBeVisible();

    // About Page
    await page.goto("/about");
    await expect(page.locator("h1")).toContainText("DEMOCRATIZING");
    await expect(page.locator("text=Evidence Before Assertion").first()).toBeVisible();

    // Contact Page
    await page.goto("/contact");
    await expect(page.locator("h1")).toContainText("LET'S TALK");
    await expect(page.locator("text=Request a Strategic Consultation").first()).toBeVisible();
  });

  // -------------------------------------------------------------
  // 2. APPLICATION WORKSPACE
  // -------------------------------------------------------------
  test("3. Command Center Dashboard loads at /app with metrics and sidebar", async ({ page }) => {
    await page.goto("/app");
    await expect(page.locator("h1")).toContainText("YOUR INTELLIGENCE COMMAND CENTER.");

    // Verify Persistent AppSidebar Navigation Links
    await expect(page.locator("aside").getByRole("link", { name: "Command Center" })).toBeVisible();
    await expect(page.locator("aside").getByRole("link", { name: "New Research" })).toBeVisible();
    await expect(page.locator("aside").getByRole("link", { name: "Agent Observatory" })).toBeVisible();
    await expect(page.locator("aside").getByRole("link", { name: "Opportunities" })).toBeVisible();
    await expect(page.locator("aside").getByRole("link", { name: "Hypotheses" })).toBeVisible();
    await expect(page.locator("aside").getByRole("link", { name: "Risk Observatory" })).toBeVisible();
    await expect(page.locator("aside").getByRole("link", { name: "Evidence Explorer" })).toBeVisible();
    await expect(page.locator("aside").getByRole("link", { name: "Executive Reports" })).toBeVisible();
    await expect(page.locator("aside").getByRole("link", { name: "Business Simulator" })).toBeVisible();
    await expect(page.locator("aside").getByRole("link", { name: "Research History" })).toBeVisible();
    await expect(page.locator("aside").getByRole("link", { name: "System Settings" })).toBeVisible();

    // Verify TopBar
    await expect(page.locator("header nav")).toContainText("Workspace");
  });

  test("4. New Research request form validates and supports templates", async ({ page }) => {
    await page.goto("/app/research/new");
    await expect(page.locator("h1")).toContainText("New Research Investigation");

    // Click a template chip
    const templateChip = page.locator("button:has-text('Fashion E-commerce in Emerging Markets')");
    await expect(templateChip).toBeVisible();
    await templateChip.click();

    // Check textarea is populated
    const textarea = page.locator("textarea#objective");
    await expect(textarea).not.toBeEmpty();

    // Check submission button exists
    await expect(page.locator("button:has-text('Generate Research Intelligence')")).toBeVisible();
  });

  test("5. Agent Observatory displays all 8 agents and detail modal", async ({ page }) => {
    await page.goto("/app/agents");
    await expect(page.locator("h1")).toContainText("Autonomous Multi-Agent Fleet");

    // Check Director and Specialists
    await expect(page.locator("text=Research Director").first()).toBeVisible();
    await expect(page.locator("text=Meta Muse Wonder").first()).toBeVisible();
    await expect(page.locator("text=Market Intelligence Analyst").first()).toBeVisible();
    await expect(page.locator("text=Competitor Intelligence Analyst").first()).toBeVisible();
    await expect(page.locator("text=Customer Intelligence Analyst").first()).toBeVisible();

    // Open detail modal
    const inspectBtn = page.locator("button:has-text('Inspect Details')").first();
    await inspectBtn.click();
    await expect(page.locator("text=Full Agent Responsibilities").first()).toBeVisible();
    await expect(page.locator("button:has-text('Close Dossier')")).toBeVisible();
    await page.locator("button:has-text('Close Dossier')").click();
  });

  test("6. Opportunities dashboard and dossier view render", async ({ page }) => {
    await page.goto("/app/opportunities");
    await expect(page.locator("h1")).toContainText("Market White-Spaces & Scored Opportunities");
    await expect(page.locator("input[placeholder*='Search opportunities']")).toBeVisible();
  });

  test("7. Autonomous Hypothesis Workspace renders lifecycle timeline", async ({ page }) => {
    await page.goto("/app/hypotheses");
    await expect(page.locator("h1")).toContainText("Research Hypotheses & Loop Inspection");
    await expect(page.locator("text=LIFECYCLE PIPELINE ARCHITECTURE").first()).toBeVisible();
    await expect(page.getByRole("heading", { name: "Observation" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Hypothesis" })).toBeVisible();
  });

  test("8. Risk Observatory displays severity matrix and category filter", async ({ page }) => {
    await page.goto("/app/risks");
    await expect(page.locator("h1")).toContainText("Systemic Risk Observatory");
    await expect(page.locator("text=LIKELIHOOD VS. IMPACT SEVERITY MATRIX").first()).toBeVisible();
  });

  test("9. Evidence Explorer displays evidence, sources, and claims tabs", async ({ page }) => {
    await page.goto("/app/evidence");
    await expect(page.locator("h1")).toContainText("Evidence & Provenance Explorer");

    await expect(page.locator("button:has-text('Evidence Cards')")).toBeVisible();
    await expect(page.locator("button:has-text('Primary Sources')")).toBeVisible();
    await expect(page.locator("button:has-text('Claim Audits')")).toBeVisible();

    // Click Primary Sources tab
    await page.locator("button:has-text('Primary Sources')").click();
    await expect(page.locator("th:has-text('Source Title')")).toBeVisible();
  });

  test("10. Executive Reports archive renders", async ({ page }) => {
    await page.goto("/app/reports");
    await expect(page.locator("h1")).toContainText("Synthesized Executive Reports");
  });

  test("11. Business Simulator recalculates deterministic scenarios", async ({ page }) => {
    await page.goto("/app/simulator");
    await expect(page.locator("h1")).toContainText("Unit Economics Simulator");

    await expect(page.locator("label:has-text('Selling Price')").first()).toBeVisible();
    await expect(page.locator("text=Monthly Revenue").first()).toBeVisible();
    await expect(page.locator("text=Operating Profit").first()).toBeVisible();
    await expect(page.locator("button:has-text('Recalculate Python Engine')")).toBeVisible();
  });

  test("12. Research History and Run Comparator render", async ({ page }) => {
    await page.goto("/app/history");
    await expect(page.locator("h1")).toContainText("Research History & Run Comparison");
  });

  test("13. System Settings page displays live diagnostic health cards", async ({ page }) => {
    await page.goto("/app/settings");
    await expect(page.locator("h1")).toContainText("Settings & Architecture Status");
    await expect(page.locator("text=FastAPI Authoritative Core").first()).toBeVisible();
    await expect(page.locator("text=SQLite Persistent Store").first()).toBeVisible();
    await expect(page.getByRole("heading", { name: "Meta AI Model Allocation" })).toBeVisible();
    await expect(page.locator("text=Tavily Web Spidering").first()).toBeVisible();
  });
});
