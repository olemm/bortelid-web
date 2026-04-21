# Project Roadmap: bortelid-web

## Phase 1: Foundation & Visual Identity
- [ ] 1.1 Implement `apps/_scaffold/templates/base.html` with Tailwind CSS and responsive nav.
- [ ] 1.2 Create `apps/_scaffold/controllers/home.py` and export it in `controllers.py`.
- [ ] 1.3 Create `apps/_scaffold/templates/home.html` with a professional Hero section.
- [ ] 1.4 Verify that `python run.py` loads the homepage correctly.

## Phase 2: Content Management System (Admin)
- [ ] 2.1 Define `pages` table schema in `apps/_scaffold/databases/pages.py`.
- [ ] 2.2 Create `apps/_scaffold/controllers/admin.py` (CRUD for pages).
- [ ] 2.3 Implement Admin views: List pages, Create/Edit page, Delete page.
- [ ] 2.4 Implement basic admin authentication/protection.

## Phase 3: Dynamic Frontend
- [ ] 3.1 Create a dynamic route in `controllers/` to fetch pages by slug from DB.
- [ ] 3.2 Implement a dynamic template that renders content/images stored in the DB.
- [ ] 3.3 Create a "Dynamic Menu" system that reads page positions from DB.

## Phase 4: Cabin Owner & Tourist Modules
- [ ] 4.1 DB Schema for Cabin Owners and Cabin details.
- [ ] 4.2 Implement Owner's Dashboard.
- [ ] 4.3 Implement Tourist Inquiry form and contact logic.

## Phase 5: Polishing & Launch
- [ ] 5.1 SEO Optimization (Meta tags, Sitemaps).
- [ ] 5.2 Performance audit (Image optimization).
- [ ] 5.3 Final UI/UX polish based on bortelid.no analysis.
