# Eval-Set JD Bodies — for `EVAL_SET.md` calibration runs

> **What this file is:** The 6 JD bodies that back `docs/EVAL_SET.md`'s gold-standard targets, extracted from `Job Posting samples/JD mapping to my exp..docx` (Ayesha's manually-labeled set, the source-of-truth that EVAL_SET.md was adapted from). Without these bodies sitting in a runner-compatible format, calibration could only re-run if every original posting was still live on the source ATS — and they're not.
>
> **How to use it:** When you want to re-run calibration (after a `SCORING_PROMPT.md` change, or as part of monthly QC):
>
> 1. `cat docs/EVAL_SET_JDS.md >> MANUAL_JDS.md`
> 2. `python scripts/score_jobs.py`
> 3. Compare the resulting `_local/digest.md` scores against the targets in `docs/EVAL_SET.md`. Any role off by > 1 point = iterate the prompt before shipping.
>
> Cost: 6 entries × ~$0.12 = ~$0.72 per run.
>
> **Why JD bodies are committed (not gitignored):** Each JD is from a public job posting at the time of capture (April 2026). They contain no personal information about Ayesha and no proprietary content from her past employer. They're functionally identical to the entries the live scrapers produce — just frozen in time so calibration stays runnable indefinitely.
>
> **Last updated:** 2026-05-03 (Session 2.2.2 — added Posting 7: Snorkel.AI Sr PM, Platform (HM-callback after warm referral, target 9) and Posting 8: Zillow/FUB Sr PM AI Platform & Ecosystem (user-judged good fit, Seattle, target 8 — likely the same role as the original Session 2.0 validation JD). Total entries now 8; full re-run cost ~$0.96 (8 × $0.12).)

---

## Wise — Senior Product Manager — Invoicing (Wise Business)
**URL:** (from `Job Posting samples/JD mapping to my exp..docx` — original posting no longer guaranteed live)
**Posted:** unknown (frozen snapshot — Job #1 (eval target 8))
**Source:** eval set (calibration)

---
Wise is a global technology company, building the best way to move and manage the world’s money. Min fees. Max ease. Full speed. Whether people and businesses are sending money to another country, spending abroad, or making and receiving international payments, Wise is on a mission to make their lives easier and save them money. As part of our team, you will be helping us create an entirely new network for the world's money. For everyone, everywhere. More about our mission and what we offer. Job Description We want to make moving money internationally instant, convenient, transparent and eventually free.  For businesses, this means helping them to do business from anywhere and expand everywhere. To help them do this, we're building a world class business bank account, which allows them to get paid and pay people no matter where they are in the world, without getting ripped off by unfair exchange rates.  Many of our customers rely on us to get paid – from sending invoices all over the world, to collecting payments via payment links. We want to build best-in-class solutions for them to get paid easier domestically and internationally, in whatever currency, payment method, or format they want. Our focus is on solving problems for high growth SMBs, and we want to help them get paid fast, reliably, and by anyone. You'll start by identifying, scoping, and shipping impactful changes in our Invoicing product for customers all over the world. From there, you’ll own our entire product suite and roadmap that aims to help businesses get paid with easy, low/no-code solutions. You’ll ultimately be responsible for growing the volume of payments that businesses collect with us, by spearheading the roadmap for building tools that fit straight into our customers’ sales and revenue workflows. You’ll collaborate with teams across all of Wise Business and over many regions to ensure that these tools work for different types of businesses all over the world. Qualifications * You have an understanding and relevant experience of building new products end-to-end, with strong focus on user experience * You have at least 5+ years experience in a PM role with demonstrable experience developing and implementing successful product strategies with measurable, successful outcomes  * You’re highly analytical and are comfortable using data - both quantitative and qualitative - to identify opportunities, prioritize initiatives and refine the product strategy. * You can demonstrate how you’ve collaborated with engineers and analysts to successfully launch a new feature or product to market and/or can demonstrate how you’ve made significant improvements to an existing product  * You’ve worked closely with back-end engineers and are comfortable making technical trade-offs to deliver faster for customers  * You’re comfortable with ambiguity and not knowing all the answers, and can take complex situations and bring structure, focus, and direction. You can unblock the team tactically and transform paralysis into action. Bonus: * You have experience building B2B software * You have experience managing 3rd party relationships
---

## Wise — Senior Product Manager — Treasury Ledger Platform
**URL:** (from `Job Posting samples/JD mapping to my exp..docx` — original posting no longer guaranteed live)
**Posted:** unknown (frozen snapshot — Job #2 (eval target 9))
**Source:** eval set (calibration)

---
Company Description
Wise is a global technology company, building the best way to move and manage the world’s money.Min fees. Max ease. Full speed.
Whether people and businesses are sending money to another country, spending abroad, or making and receiving international payments, Wise is on a mission to make their lives easier and save them money.
As part of our team, you will be helping us create an entirely new network for the world's money.For everyone, everywhere.
More about our mission and what we offer.
Job Description
Your Mission: Data Integrity, Real timeliness, and Controls
Your mandate is to build and maintain the foundational Treasury Ledger platform that guarantees the real time integrity and compliance of every transaction across Wise’s global ecosystem. The systems you own secure the integrity of our cross currency monthly volume across all of Wise. You will also transform the platform from a  ledgering tool into a proactive control mechanism. 
Your impact:  The Core of Global Treasury Operations
Within the Treasury Product team, you will lead the Treasury Ledger workstream. This system is the unquestionable source of truth for:
Financial Visibility: Providing a real-time, globally reconciled view of cross-currency exposures, cash balances, and liquidity funding requirements 
Control and Auditability: Designing, owning, and implementing the definitive controls framework within the ledger (e.g., balance integrity checks, reconciliation processes) to ensure completeness, accuracy, and compliance.
Downstream Execution: Empowering critical teams with actionable, trusted data, including Traders (for execution and hedging) and Operational teams (for money movement, settlement, and reconciliation).
Organisational Role: Your team's systems are the single source of consumable data (the ledger of record) that underpins all critical downstream functions, including hedging, safeguarding, as well as strategic decision-making by executive leadership.
The Scale: You will be leading the vision for a ledgering system currently processing over 2bn+ journal entries a month.
You will also be owning the processes around prioritising and Implementing new product flows into the Ledger 
The core questions that you will answer in your role are -
How do you build systems and controls that ensure completeness and accuracy of product flows?
How do you identify and eliminate operational risks?
You will define and execute the product strategy to achieve real-time reconciliation and assurance at global scale, providing treasury teams with systems they need to operate effectively, compliantly, and efficiently across  currencies
Qualifications
What we’re looking for: 
Domain Understanding 
Understanding of treasury systems in either an engineering, data or product role
Product Management Excellence 
Multiple years of product building experience, either as an engineering or product or operations leader in a hands-on role. 
Proven technical leadership: You are not just willing, but capable and expected to deep-dive into the technical architecture with discussions with engineers. This includes taking part in the the decision-making process around ledger design, data models, infrastructure choices etc
Strong individual contributor, willing to get your hands dirty and build product yourself. Typically will have a background that shows they have a superpower (engineer, analyst, consultant, serial entrepreneur, etc).
Held multiple product roles, and can draw on different experiences and roles when forming opinions and executing. 
Have defined and moved KPIs with features shipped.
Have built roadmaps for teams finding a path from uncertainty/chaos to clarity 
Leadership 
Extensive Treasury experience, especially within complex, high-volume financial technology or banking environments.
Flexible in approach - not stuck to a “by the book” product role definition.
Enthusiastic about learning new skills to unblock yourself and your team. 
Problem Solving 
Analytically-minded, can clearly frame problems, articulate hypotheses and solutions, measure them and has used the tools to be able to do this without an analyst
Showcases system-level thinking, a proven ability to look beyond the scope of a single product to design interconnected systems
Nice-to-haves: 
Treasury, Finance or  experience particularly in Ledgers
Experience with Controls or Audits
---

## Liberis — Senior Product Manager — Financial Systems
**URL:** (from `Job Posting samples/JD mapping to my exp..docx` — original posting no longer guaranteed live)
**Posted:** unknown (frozen snapshot — Job #3 (eval target 8))
**Source:** eval set (calibration)

---
About our Product Team: Liberis is building the embedded finance platform that lets partners around the world offer innovative funding products to their small business customers. We're a growth-stage fintech with teams in London, Atlanta, Stockholm, Munich and Mumbai, and we're at a point where the platform challenges are genuinely interesting: we're not just adding features, we're building financial infrastructure that didn't exist a year ago. Engineering is going through an AI-first transformation, rethinking how teams are structured and how they ship. It's changing what a small team can do. Product owns outcomes here, not just delivery. You will have real autonomy, a direct partnership with engineering leadership, and the space to make big calls on hard problems. If you've spent time in large organisations waiting for permission, this is different. The role: We are looking for a Senior Product Manager to own our Financial Systems domain. This is a role for someone who thinks in systems, not features. You will own the foundational layers that the rest of Liberis builds on top of: the payment rails, ledger, merchant revenue intelligence, and identity systems that make our products work. The problems here are genuinely hard. How do you replace a third-party classification engine with an in-house AI model without disrupting live underwriting? How do you build a new repayment capability that opens up partners who sit outside the payment flow? How do you manage payment infrastructure across multiple providers and geographies while migrating the platform underneath? If these are the kinds of challenges that get you out of bed, keep reading. You will partner directly with a Head of Engineering and work across several small, focused engineering teams. We're in the middle of an AI-first engineering transformation: teams of 2-4 engineers work on a problem but execute like a full team, with AI embedded in how they build, test, and ship. There are around 20 engineers across the domain, and the way they work is changing fast. You'll be part of shaping that. What you'll get to do: Own the product vision, roadmap and delivery across Financial Systems (Funding, Ledger, Merchant Revenue) and Merchant Identity. Lead complex platform initiatives end-to-end: vendor-to-AI transitions, new payment rail buildouts, cross-provider infrastructure management, and data model evolution. Several of these involve replacing legacy vendor systems with in-house AI models. These aren't feature requests. They're engineering-heavy, cross-team programmes with real commercial stakes. Sit with engineers daily. Understand the data flows and the API contracts. Be the PM who engineers want in the room because you make technical decisions better, not slower. Drive cross-functional alignment on initiatives that require buy-in from Risk, Finance, Commercial, and Engineering leadership. Build business cases, present pilot data, and make the commercial argument for platform investment. Manage vendor relationships and make build-vs-buy decisions with real contract deadlines and cost implications. Build technical roadmaps that balance architectural health with commercial delivery. Sequence migrations so the business keeps shipping while the platform improves underneath. Who you are: A systems thinker. When someone describes a requirement, you think about the data model underneath, the identity resolution upstream, and the three teams whose work will break if you get this wrong. You find the edge cases before engineering does. Technically deep. You can read a schema, follow a data flow, and have a real conversation with engineers about API design, migration strategies, and system trade-offs. You don't write production code, but engineers respect your judgement because you've earned it. Comfortable with complexity. The domains you will own don't have neat boundaries. Merchant identity touches everything. Financial systems underpin every product. You have led large migrations, platform consolidations, or system redesigns and know that the hard part is sequencing, not architecture. Execution driven. You break large, intimidating platform programmes into deliverable increments. You keep momentum through complexity rather than getting lost in it. Commercially grounded. You can articulate why replacing a vendor saves six figures a year, why a new repayment method unlocks a major revenue stream, or why a migration matters for speed to market. You bring skeptical stakeholders along with data, not slides. A clear communicator. You adjust naturally between a technical deep-dive with an engineer and a strategic update for the exec team. You write well, present clearly, and keep stakeholders informed without being asked. What we think you'll need: Experience owning platform or infrastructure-level product areas: data platforms, identity systems, ledgers, core banking, payments infrastructure, or similar. A track record of leading complex migrations, vendor transitions, or platform redesigns in production, with real deadlines and commercial pressure. Experience in fintech, lending, payments or financial services. You understand payment rails, revenue-based finance, and the regulatory context around financial products. Strong data skills and genuinely excited about using AI tooling to move faster, whether that's interrogating data, drafting specs, or accelerating your own workflow. You'll be joining an org that's betting heavily on AI across both its products and its ways of working.
---

## Ebury — (Senior) Product Manager — API Platform & Developer Experience
**URL:** (from `Job Posting samples/JD mapping to my exp..docx` — original posting no longer guaranteed live)
**Posted:** unknown (frozen snapshot — Job #4 (eval target 6))
**Source:** eval set (calibration)

---
Ebury helps ambitious businesses unlock global growth, and we take the same approach with our people. We encourage innovation and movement, collaboration and problem-solving, and foster an environment where everyone can feel they belong, are valued, supported and empowered to succeed. If you’re a collaborator who wants to help transform how businesses operate globally, get in touch - we’d love to discuss how Ebury can accelerate your career so you can shape the future. __(Senior) Product Manager - API Platform & Developer Experience__ Product - API Team Ebury London Office - Hybrid: 4 days in the office, 1 day working from home per week We are looking for a technically strong (Senior) Product Manager to help grow and evolve our API platform and API use cases. This role focuses on building high-quality, scalable APIs that enable partners and clients to integrate deeply with our payments, FX, and financial services capabilities. You will work closely with engineering, design, and commercial teams to define new endpoints, webhooks, and workflows, while ensuring excellent developer experience and platform reliability.  The role sits at the heart of Ebury's platform strategy.  What you’ll do API Product ownership * Own parts (or all) of the API platform and use-case roadmap * Define and evolve API endpoints, webhooks, error models, and data contracts * Ensure APIs are consistent, versioned, and easy to integrate with  Technical collaboration         - Work closely with backend and frontend engineers on: * API design and best practices * Authentication and authorization flows * Webhooks, retries and idempotency       -  Participate actively in technical and trade-offs Delivery & Execution * Translate business and partner needs into clear product requirements * Drive delivery from discovery through launch and iteration * Balance short-term delivery with long-term platform scalability Stakeholder management * Partner with Payments, FX, Compliance, Risk, and Operations teams * Support Sales and Partnerships with API capabilities and use cases * Act as a product representative for API consumers (internal and external)  Developer experience      -  Collaborate with the DevEx team on: * Documentation and onboarding * Sandbox and testing environments * Observability and error reporting      -   User developer feedback to continuously improve the API experience What success looks like * New API use cases launched and adopted by partners * Reduced integration time for new API consumers * Clear, stable, and well-documented APIs and developer guides * Positive developer feedback and reduced support friction * Increased API coverage of Ebury’s services * Substantial growth in number of API users  What you’ll need * 3+ years of Product Management experience (L3)  * 5+ years (L4) / 7+ years (L5) * Strong experience working on API-first or platform products * Comfortable reading and discussing technical designs and trade-offs * Experience defining APIs, webhooks, and integration patterns * Strong communication skills with both technical and non-technical stakeholders Preferred experience * Fintech, payments, FX, or financial infrastructure experience * Experience with: REST APIs (GraphQL a plus), OAuth 2.0, API keys, and authentication models, Event-driven systems and webhooks * Experience working with external developers or partners Level-specific expectations     Product Manager II (L3) * Own well-defined API areas or features * Execute against a clear roadmap with guidance * Write strong product requirements and API specs * Learn the domain and grow technical depth     Senior Product Manager (L4) * Own major API surfaces or end-to-end use cases * Drive discovery and delivery independently * Make trade-offs balancing customer needs and platform health * Influence API standards and best practices
---

## Boku — Growth Product Manager — Subscription Products
**URL:** (from `Job Posting samples/JD mapping to my exp..docx` — original posting no longer guaranteed live)
**Posted:** unknown (frozen snapshot — Job #5 (eval target 3))
**Source:** eval set (calibration)

---
Boku Inc. (BOKU.L) is the leading global provider of local mobile-first payments solutions. Global brands including Amazon, DAZN, Meta, Google, Microsoft, Netflix, Sony, Spotify, and Tencent rely on Boku to reach millions of new paying consumers who do not use credit cards with our purpose-built payment network of more than 300 local payment methods across 70+ countries. Every year, Boku processes over $10 billion in value for our customers. Incorporated in 2008, Boku is headquartered in London and San Francisco and has employees in over 39 countries around the world, including Brazil, China, Estonia, Germany, Ireland, Japan, Singapore, and the UAE. Boku is a truly global company that takes pride in its diversity and thriving equal opportunity workplace.
Role Summary 
We’re hiring a Growth Product Manager (GPM) to help build and scale our product-led growth capabilities across our subscription products, as we evolve towards a more structured and scalable growth engine. You’ll play a key role in improving conversion from signup to first value and long-term retention. You will own a key area of the customer lifecycle and its associated KPIs, driving the strategy, roadmap, and execution of growth initiatives across acquisition, activation, retention, or expansion.  This is a hands-on role focused on running experiments, improving onboarding and shipping growth features to increase conversion, engagement, and revenue.  You will also help establish funnel metrics, support the development of our growth strategy, and bring more structure and speed to how we execute growth. Working closely with Core Product Management, Commercial, Product Marketing, and Data Product Management you’ll contribute to building a more systematic, data-driven approach to growth and delivering measurable business impact. 
Key Responsibilities 
Own and drive growth across the funnel 
Own a key stage of the customer lifecycle (acquisition, activation, retention, or expansion) and its associated KPIs
Identify and prioritize the highest-impact opportunities to improve conversion, retention, and revenue
Define and track key growth metrics across the funnel (e.g., activation, retention, NRR), working with data teams to generate insights, evaluate experiments, and guide decisions 
Run experiments and optimize user journeys 
Design, run, and analyze experiments to improve onboarding, activation, engagement, and expansion
Ship product changes and growth features based on experiment results and customer insights
Continuously iterate on user journeys to improve time-to-value, conversion, and long-term retention 
Improve acquisition, conversion, and expansion
Own and optimize the end-to-end acquisition funnel, partnering with commercial teams to improve conversion across sales-led journeys from lead to activation 
Increase lead quality, conversion rates, and speed through the funnel
Identify and execute upsell, cross-sell, and product adoption opportunities to drive revenue growth 
 Collaborate to deliver growth impact
Own and drive growth initiatives end-to-end, partnering with Core Product, Data Product, Commercial, Product Marketing and Marketing 
Use data and customer insights (e.g., interviews, surveys, behavioural data) to identify growth opportunities and inform product decisions
Help establish scalable experimentation practices and improve how we use data to drive growth decisions 
Key Skills and Competencies 
3-5 years of experience in growth product management or a similar role, with a focus on B2B markets
Strong knowledge of growth frameworks (AARRR, North Star Metric)
Experience with experimentation and A/B testing
Ability to prioritize using RICE/ICE methodologies
Proven skills in funnel analysis and conversion optimization
Customer-centric approach using frameworks like JTBD
Proven track record of driving measurable growth in SaaS or enterprise product environments
Strong understanding of B2B growth dynamics, including lifecycle management and sales funnel optimization
Data-driven mindset, with proficiency in analytics tools and CRM platforms
Technical fluency, including experience working with APIs and technical documentation
Strong cross-functional collaboration skills, with the ability to work closely with internal stakeholder teams to deliver growth-focused product features
Excellent communication and stakeholder management, with a proven ability to align teams around shared goals
Strategic thinking combined with hands-on execution, able to move from insight to impact quickly
Fluency in Mandarin (spoken and written) is required.
Preferred Qualifications 
Experience working in SaaS, enterprise, or mid-market B2B environments.
Familiarity with growth frameworks such as Product-Led Growth (PLG) and Customer Success-Led Growth.
Knowledge of financial metrics like ARR, MRR, and LTV/CAC ratios.
---

## Rippling — Product Lead — Talent Management
**URL:** (from `Job Posting samples/JD mapping to my exp..docx` — original posting no longer guaranteed live)
**Posted:** unknown (frozen snapshot — Job #6 (eval target 2))
**Source:** eval set (calibration)

---
About Rippling
Rippling gives businesses one place to run HR, IT, and Finance. It brings together all of the workforce systems that are normally scattered across a company, like payroll, expenses, benefits, and computers. For the first time ever, you can manage and automate every part of the employee lifecycle in a single system.Take onboarding, for example. With Rippling, you can hire a new employee anywhere in the world and set up their payroll, corporate card, computer, benefits, and even third-party apps like Slack and Microsoft 365—all within 90 seconds.Based in San Francisco, CA, Rippling has raised $1.85B+ from the world’s top investors—including Kleiner Perkins, Founders Fund, Sequoia, Greenoaks, and Bedrock—and was named one of America's best startup employers by Forbes.We prioritize candidate safety. Please be aware that all official communication will only be sent from @__Rippling.com__ addresses.About The RoleThe Talent Management team owns a suite of products that help Rippling customers manage, develop, and retain their employees.As a Product Lead on the Talent Management team, you will play a pivotal role in shaping the direction of this initiative by owning the vision, strategy, and execution for a core set of products within the suite. You will work cross-functionally with engineering, design, data science, and go-to-market teams to deliver innovative solutions that help managers become better leaders and employees grow in their careers. You will own the roadmap for your product area, determining which capabilities the team should invest in based on a deep understanding of customer needs, the competitive landscape, and Rippling’s unique strengths.What You Will Do * Define and execute the product vision, strategy, and roadmap for a portfolio of products within the Talent Management suite. * Collaborate closely with engineering, design, data science, and go-to-market teams to launch innovative features that help managers become better leaders. * Deeply understand the competitive landscape and customer needs to prioritize investments and ensure product-market fit for the products you own. * Define and analyze key success metrics to measure the adoption, impact, and business value of your product area. * Identify and execute on opportunities to integrate insights from your products into other areas of the Rippling platform, maximizing their value for customers. What You Will Need * 8+ years of Product Management experience. * Self-starter with a bias towards action. * Ability to thrive in a fast-paced environment. * Strong product and usability instincts. * Helicopter pilot mentality: you can easily switch from high-level strategy and planning to UI polish and data model details. * Exceptional written and verbal communication skills. * Experience building complex workflows and integration/marketplace products. * Founder or hyper-growth startup experience a strong plus. * Strong alignment with our __leadership principles__: in particular Go and See, Push the Limits of Possible, and Are Right, a Lot.
*****************************************
---

## Snorkel.AI — Senior Product Manager — Platform
**URL:** (supplied by Ayesha during session 2026-05-03 — original posting may or may not still be live)
**Posted:** unknown (frozen snapshot — Job #7 (eval target 9; HM-callback after warm referral))
**Source:** eval set (calibration)

---
About Snorkel

At Snorkel, we believe meaningful AI doesn't start with the model, it starts with the data.

We're on a mission to help enterprises transform expert knowledge into specialized AI at scale. The AI landscape has gone through incredible changes between 2015, when Snorkel started as a research project in the Stanford AI Lab, to the generative AI breakthroughs of today. But one thing has remained constant: the data you use to build AI is the key to achieving differentiation, high performance, and production-ready systems. We work with some of the world's largest organizations to empower scientists, engineers, financial experts, product creators, journalists, and more to build custom AI with their data faster than ever before. Excited to help us redefine how AI is built? Apply to be the newest Snorkeler!

The Role

We are seeking a Senior Product Manager to own the core platform that powers all data operations across our ecosystem. This platform enables experts to efficiently produce high-quality data, supports internal operations at scale, and provides reliable APIs and SDKs for customers.

In this role, you will own the end-to-end experience of our data platform — from expert tooling and workflow orchestration, to identity and access management, data ingestion, versioning, and delivery. You will define platform strategy, set the roadmap, and partner closely with Engineering, Research, and Operations to build scalable, reliable systems that support high-throughput, high-quality data production.

This is a highly cross-functional, technically deep IC role with broad surface area and significant impact. You will lead initiatives spanning multiple teams, balancing near-term execution with long-term platform evolution.

What You'll Do

Own the product vision, strategy, and roadmap for the core platform supporting expert contributors, internal operations, and customers.

Define and deliver expert tooling, workflow orchestration systems, and internal ops controls that improve productivity, quality, and scalability.

Lead platform initiatives across data ingestion, storage, versioning, permissions/IAM, and system reliability.

Partner deeply with Engineering to make informed tradeoffs across APIs, data models, system architecture, and platform abstractions.

Collaborate with Research and Operations to ensure platform capabilities support evolving RLHF methodologies and operational needs.

Build and evolve APIs and SDKs that enable customers to seamlessly access the platform capabilities

Drive metrics across throughput, cycle time, quality, cost efficiency, platform adoption, and reliability.

Identify platform bottlenecks and lead cross-team efforts to improve performance, scalability, and experts experience.

Balance short-term delivery with long-term platform investments to support future growth.

Minimum Qualifications

5–7 years of experience as a Product Manager, with ownership of complex, cross-functional product areas.

Experience building internal tools, ops platforms, or data platforms at scale.

Strong technical fluency, with comfort discussing APIs, data models, system design, and infrastructure tradeoffs with engineering teams.

Proven ability to own end-to-end product experiences across multiple user personas.

Strong analytical and problem-solving skills, with a track record of metrics-driven decision making.

Excellent collaboration skills and experience partnering closely with Engineering, Research, and Operations teams.

Preferred Qualifications

Experience building platforms that support human-in-the-loop or data production workflows.

Background in data infrastructure, ML platforms, or enterprise SaaS products.

Experience designing APIs or developer-facing platforms.

Demonstrated ability to lead large, cross-team initiatives without formal authority.
---

## Zillow Group (Follow Up Boss) — Senior Product Manager — AI Platform & Ecosystem
**URL:** (supplied by Ayesha during session 2026-05-03 — original posting may or may not still be live)
**Posted:** unknown (frozen snapshot — Job #8 (eval target 8; user-judged good fit, Seattle, H1B sponsor))
**Source:** eval set (calibration)

---
About the team

Follow Up Boss (FUB), part of Zillow Group, is a leading CRM for high-performing real estate teams, serving more than 100,000 agents. Our mission is to help agents deliver exceptional client experiences, run their business with ease, and win more deals. Within the FUB Product organization, this team is building the AI platform and ecosystem capabilities that power the next generation of product experiences, helping agents spend less time navigating software and more time building relationships.

About the role

We're looking for a Senior Product Manager to help shape how AI works across Follow Up Boss. In this role, you'll lead the platform capabilities that connect AI to FUB's data, workflows, and integrations, making it possible to build smarter, more useful experiences for agents. You'll influence how AI-powered experiences understand context, take action, and become more personalized over time. This is a high-impact opportunity to define platform strategy, partner deeply with cross-functional teams, and help turn emerging AI capabilities into meaningful customer and business value.

You Will Get To

Own the strategy and evolution of the platform capabilities that enable AI assistants, workflows, and integrations to interact with Follow Up Boss in reliable, scalable ways.

Define how internal AI systems and external partners connect to FUB data and actions through clear, well-designed tools and integration patterns.

Shape the context and intelligence capabilities that help AI better understand agent and lead activity, including signals, summaries, and data quality improvements.

Lead the product direction for memory capabilities that make AI experiences more personalized and useful across interactions over time.

Partner closely with engineering, AI/ML, design, and product peers to assess tradeoffs, define solutions, and ship iteratively.

Help identify and prioritize the highest-value platform and ecosystem opportunities based on product needs, usage patterns, and long-term strategy.

Drive alignment across teams by communicating roadmap priorities, progress, and strategic decisions clearly to stakeholders and leadership.

Contribute to the long-term vision for how AI platform capabilities show up in product experiences across web, mobile, automation, and assistant surfaces.

This role has been categorized as a Remote position. "Remote" employees do not have a permanent corporate office workplace and, instead, work from a physical location of their choice, which must be identified to the Company. U.S. employees may live in any of the 50 United States, with limited exceptions.

In California, Connecticut, Maryland, Massachusetts, New Jersey, New York, Washington state, and Washington DC the standard base pay range for this role is $148,600.00 - $237,400.00 annually. This base pay range is specific to these locations and may not be applicable to other locations.

In Colorado, Hawaii, Illinois, Minnesota, Nevada, Ohio, Rhode Island, and Vermont the standard base pay range for this role is $141,200.00 - $225,600.00 annually. The base pay range is specific to these locations and may not be applicable to other locations.

In addition to a competitive base salary this position is also eligible for equity awards based on factors such as experience, performance and location. Actual amounts will vary depending on experience, performance and location. Employees in this role will not be paid below the salary threshold for exempt employees in the state where they reside.

Who you are

5+ years of product management experience, ideally in platform, infrastructure, AI, LLMs, workflow, or other technically complex product spaces.

Strong technical fluency and the ability to work closely with engineers on APIs, integrations, data models, and system design decisions.

Experience building AI-powered products, with a strong understanding of how tools, context, memory, evaluation, and reliability come together in real product experiences.

A systems-oriented mindset and the ability to think beyond individual features to design capabilities that support multiple use cases and consumers.

A track record of defining success metrics, using data to measure impact, and making strong product decisions in ambiguous environments.

Clear communication skills, including the ability to translate complex ideas into strong product thinking, crisp documentation, and aligned execution.

A bias for action, strong judgment, and comfort balancing speed with long-term quality in a fast-moving environment.

Experience with CRMs, workflow automation, B2B SaaS, external integrations, or adjacent AI platform capabilities is a plus.

Here at Zillow - we value the experience and perspective of candidates with non-traditional backgrounds. We encourage you to apply if you have transferable skills or related experiences.
---
