#!/usr/bin/env python3
"""Update careers.html:
  1. Replace 6 placeholder job cards with 4 real Indeed job roles
  2. Wire "Apply now" to per-role modals (not the general form)
  3. Remove sample-listings banner
  4. Add modal CSS + HTML + JS
"""
from pathlib import Path

p = Path('/Users/navjotsinghhundal/W13Uk/careers.html')
html = p.read_text()

# ── 1. ROLES SECTION (old → new) ─────────────────────────────────────────────
OLD_ROLES = '''        <div class="roles-placeholder-banner" title="For internal team: replace these with live listings as they are confirmed"><i class="fas fa-info-circle"></i> Sample listings &mdash; team to update with live roles</div>
        <div class="roles-grid">
            <div class="role-card">
                <span class="role-card-tag">Land &amp; Planning</span>
                <h3 class="role-card-title">Senior Land Manager</h3>
                <div class="role-card-meta"><span><i class="fas fa-map-marker-alt"></i> Birmingham</span><span><i class="fas fa-briefcase"></i> Full-time</span></div>
                <p class="role-card-desc">Lead site identification, appraisal and acquisition across the Midlands. Proven track record sourcing residential and mixed-use opportunities of 50 units and above.</p>
                <a href="#apply" class="role-card-link">Apply now <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
            </div>
            <div class="role-card">
                <span class="role-card-tag">Planning</span>
                <h3 class="role-card-title">Planning Consultant</h3>
                <div class="role-card-meta"><span><i class="fas fa-map-marker-alt"></i> Birmingham / Hybrid</span><span><i class="fas fa-briefcase"></i> Full-time</span></div>
                <p class="role-card-desc">Prepare and submit planning applications, coordinate consultant teams and engage with local authorities. RTPI accreditation preferred. 3+ years post-qualification experience.</p>
                <a href="#apply" class="role-card-link">Apply now <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
            </div>
            <div class="role-card">
                <span class="role-card-tag">Design</span>
                <h3 class="role-card-title">Project Architect</h3>
                <div class="role-card-meta"><span><i class="fas fa-map-marker-alt"></i> Birmingham</span><span><i class="fas fa-briefcase"></i> Full-time</span></div>
                <p class="role-card-desc">Take residential and mixed-use schemes from concept through to delivery. ARB registered with strong Revit skills and an interest in placemaking and sustainable design.</p>
                <a href="#apply" class="role-card-link">Apply now <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
            </div>
            <div class="role-card">
                <span class="role-card-tag">Delivery</span>
                <h3 class="role-card-title">Senior Project Manager</h3>
                <div class="role-card-meta"><span><i class="fas fa-map-marker-alt"></i> West Midlands</span><span><i class="fas fa-briefcase"></i> Full-time</span></div>
                <p class="role-card-desc">Run multiple live residential developments from pre-construction through handover. Strong commercial awareness, programme management and main-contractor liaison.</p>
                <a href="#apply" class="role-card-link">Apply now <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
            </div>
            <div class="role-card">
                <span class="role-card-tag">Site</span>
                <h3 class="role-card-title">Site Manager</h3>
                <div class="role-card-meta"><span><i class="fas fa-map-marker-alt"></i> West Midlands</span><span><i class="fas fa-briefcase"></i> Full-time</span></div>
                <p class="role-card-desc">Day-to-day site running, sub-contractor coordination and health &amp; safety leadership on residential schemes. SMSTS, CSCS Black Card and First Aid required.</p>
                <a href="#apply" class="role-card-link">Apply now <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
            </div>
            <div class="role-card">
                <span class="role-card-tag">Consultancy</span>
                <h3 class="role-card-title">Development Consultant</h3>
                <div class="role-card-meta"><span><i class="fas fa-map-marker-alt"></i> Birmingham / Hybrid</span><span><i class="fas fa-briefcase"></i> Full-time</span></div>
                <p class="role-card-desc">Support clients across feasibility, viability and master-developer engagements. Mixed development background &mdash; planning, design or land &mdash; with strong analytical skills.</p>
                <a href="#apply" class="role-card-link">Apply now <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
            </div>
        </div>'''

NEW_ROLES = '''        <div class="roles-grid">
            <div class="role-card">
                <span class="role-card-tag">Commercial</span>
                <h3 class="role-card-title">Chartered Quantity Surveyor</h3>
                <div class="role-card-meta">
                    <span><i class="fas fa-map-marker-alt"></i> Birmingham, B15 3BE</span>
                    <span><i class="fas fa-briefcase"></i> Permanent &middot; Full-time</span>
                </div>
                <p class="role-card-desc">Join our team to support cost management and contract administration across residential, development, and regeneration projects — from tender through to final account. RICS chartership (MRICS) desirable.</p>
                <button type="button" class="role-card-link" onclick="openApplyModal('Chartered Quantity Surveyor')">Apply now <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></button>
            </div>
            <div class="role-card">
                <span class="role-card-tag">Design</span>
                <h3 class="role-card-title">Architect &ndash; Residential Developments</h3>
                <div class="role-card-meta">
                    <span><i class="fas fa-map-marker-alt"></i> Birmingham, B15 3BE</span>
                    <span><i class="fas fa-briefcase"></i> Permanent &middot; Full-time</span>
                </div>
                <p class="role-card-desc">Lead residential design proposals from early concept through to technical delivery. ARB-registered with experience on UK housing and mixed-use projects. Proficiency in AutoCAD and/or Revit required.</p>
                <button type="button" class="role-card-link" onclick="openApplyModal('Architect \u2013 Residential Developments')">Apply now <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></button>
            </div>
            <div class="role-card">
                <span class="role-card-tag">Design</span>
                <h3 class="role-card-title">Part 2 Architectural Assistant</h3>
                <div class="role-card-meta">
                    <span><i class="fas fa-map-marker-alt"></i> Birmingham</span>
                    <span><i class="fas fa-briefcase"></i> Full-time &middot; &pound;12.21&ndash;&pound;18.56/hr</span>
                </div>
                <p class="role-card-desc">Work across all RIBA stages on residential-led development projects — contributing to design development, technical documentation, and planning submissions. Revit proficiency preferred. Portfolio required.</p>
                <button type="button" class="role-card-link" onclick="openApplyModal('Part 2 Architectural Assistant')">Apply now <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></button>
            </div>
            <div class="role-card">
                <span class="role-card-tag">Commercial</span>
                <h3 class="role-card-title">Quantity Surveyor</h3>
                <div class="role-card-meta">
                    <span><i class="fas fa-map-marker-alt"></i> Birmingham, West Midlands</span>
                    <span><i class="fas fa-briefcase"></i> Full-time</span>
                </div>
                <p class="role-card-desc">Manage costs and commercial performance across residential and commercial projects from inception to completion. Prepare cost estimates, support procurement, monitor budgets, and manage variations. Salary negotiable.</p>
                <button type="button" class="role-card-link" onclick="openApplyModal('Quantity Surveyor')">Apply now <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></button>
            </div>
        </div>'''

assert OLD_ROLES in html, 'OLD_ROLES block not found'
html = html.replace(OLD_ROLES, NEW_ROLES, 1)

# ── 2. ADD MODAL CSS before closing </style> of inline style block ─────────────
MODAL_CSS = '''
        /* --- Apply Modal --- */
        .apply-modal-overlay{position:fixed;inset:0;z-index:9000;background:rgba(9,28,51,0.88);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;padding:24px;opacity:0;visibility:hidden;transition:opacity 0.3s,visibility 0.3s}
        .apply-modal-overlay.open{opacity:1;visibility:visible}
        .apply-modal{background:#0C233F;border:1px solid rgba(68,192,192,0.18);border-radius:16px;padding:44px 48px;width:100%;max-width:640px;max-height:90vh;overflow-y:auto;position:relative;transform:translateY(20px);transition:transform 0.35s cubic-bezier(0.16,1,0.3,1)}
        .apply-modal-overlay.open .apply-modal{transform:translateY(0)}
        .apply-modal-close{position:absolute;top:18px;right:22px;background:none;border:none;font-size:22px;color:rgba(234,234,234,0.45);cursor:pointer;line-height:1;padding:4px 8px;transition:color 0.2s}
        .apply-modal-close:hover{color:#EAEAEA}
        .apply-modal-label{font-size:11px;font-weight:600;letter-spacing:2.5px;text-transform:uppercase;color:#44C0C0;margin-bottom:10px}
        .apply-modal-title{font-weight:600;font-size:clamp(20px,3vw,26px);color:#fff;line-height:1.25;margin-bottom:28px}
        .apply-modal .form-row{margin-bottom:18px}
        .apply-modal .btn-submit{width:100%;justify-content:center}
        @media(max-width:600px){.apply-modal{padding:32px 22px}}'''

# Insert before the last </style> in the <head>
close_style = '        @media (max-width:768px){'
assert close_style in html
html = html.replace(
    '        @media (max-width:768px){',
    MODAL_CSS + '\n        @media (max-width:768px){',
    1
)

# ── 3. INSERT MODAL HTML before <main> ────────────────────────────────────────
MODAL_HTML = '''<!-- APPLY MODAL -->
<div class="apply-modal-overlay" id="applyModalOverlay" role="dialog" aria-modal="true" aria-labelledby="applyModalTitle">
    <div class="apply-modal">
        <button class="apply-modal-close" onclick="closeApplyModal()" aria-label="Close">&times;</button>
        <div class="apply-modal-label">Apply Now</div>
        <h2 class="apply-modal-title" id="applyModalTitle">Role</h2>

        <form id="applyModalForm" action="https://api.web3forms.com/submit" method="POST" novalidate>
            <input type="hidden" name="access_key" value="9cdae4fd-e5b5-48fd-975e-2ebf489e6fa8">
            <input type="hidden" name="from_name" value="W13 Careers Application">
            <input type="hidden" id="modalRoleField" name="role_applied_for" value="">
            <input type="hidden" id="modalSubjectField" name="subject" value="">
            <input type="checkbox" name="botcheck" style="display:none;">

            <div class="form-row">
                <div class="form-group">
                    <label for="modal_first_name">First Name <span class="req">*</span></label>
                    <input type="text" id="modal_first_name" name="first_name" placeholder="Jane" required>
                </div>
                <div class="form-group">
                    <label for="modal_last_name">Last Name <span class="req">*</span></label>
                    <input type="text" id="modal_last_name" name="last_name" placeholder="Smith" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="modal_email">Email <span class="req">*</span></label>
                    <input type="email" id="modal_email" name="email" placeholder="jane@example.com" required>
                </div>
                <div class="form-group">
                    <label for="modal_phone">Phone</label>
                    <input type="tel" id="modal_phone" name="phone" placeholder="07000 000000">
                </div>
            </div>

            <div class="form-row full">
                <div class="form-group">
                    <label for="modal_cv_link">CV or LinkedIn Link</label>
                    <input type="url" id="modal_cv_link" name="cv_link" placeholder="https://www.linkedin.com/in/yourprofile">
                </div>
            </div>

            <div class="form-row full">
                <div class="form-group">
                    <label for="modal_message">Cover Message <span class="req">*</span></label>
                    <textarea id="modal_message" name="message" placeholder="Briefly describe your background and why you&#39;re a great fit for this role." required></textarea>
                </div>
            </div>

            <div class="form-consent">
                <input type="checkbox" id="modal_consent" name="consent" required>
                <label for="modal_consent">I consent to W13 Group processing my information for recruitment purposes. See our <a href="privacy-policy.html">Privacy Policy</a>.</label>
            </div>

            <button type="submit" class="btn-submit" id="modalSubmitBtn">
                Submit Application
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
            </button>
            <div id="modalFormStatus" class="form-status" role="status" aria-live="polite"></div>
        </form>

        <div id="modalFormSuccess" class="form-success" style="display:none;">
            <div class="form-success-icon"><i class="fas fa-check-circle"></i></div>
            <h3>Application received.</h3>
            <p>Thank you for applying for the <strong id="modalSuccessRole"></strong> role. A member of our team will be in touch shortly.</p>
        </div>
    </div>
</div>

'''

assert '<main id="main">' in html
html = html.replace('<main id="main">', MODAL_HTML + '<main id="main">', 1)

# ── 4. UPDATE JS block ────────────────────────────────────────────────────────
OLD_JS = '''<script>
function toggleMenu(){var m=document.getElementById('fullscreenMenu');if(m)m.classList.toggle('active');}
(function(){var n=document.getElementById('navbar');if(!n)return;window.addEventListener('scroll',function(){n.classList.toggle('scrolled',window.pageYOffset>100);});})();

document.getElementById('careersForm').addEventListener('submit', async function(e){
    e.preventDefault();
    var form = this;
    var status = document.getElementById('formStatus');
    var success = document.getElementById('formSuccess');
    status.className = 'form-status visible';
    status.textContent = 'Sending...';
    var formData = new FormData(form);
    try {
        var res = await fetch('https://api.web3forms.com/submit', {
            method: 'POST',
            body: formData
        });
        var data = await res.json();
        if (data.success) {
            form.style.display = 'none';
            status.classList.remove('visible');
            success.classList.add('visible');
            success.scrollIntoView({behavior: 'smooth', block: 'center'});
        } else {
            status.className = 'form-status visible error';
            status.textContent = data.message || 'Something went wrong. Please try again or email info@w13uk.com.';
        }
    } catch (err) {
        status.className = 'form-status visible error';
        status.textContent = 'Network error. Please try again or email info@w13uk.com.';
    }
});
</script>'''

NEW_JS = '''<script>
function toggleMenu(){var m=document.getElementById('fullscreenMenu');if(m)m.classList.toggle('active');}
(function(){var n=document.getElementById('navbar');if(!n)return;window.addEventListener('scroll',function(){n.classList.toggle('scrolled',window.pageYOffset>100);});})();

// ── Apply Modal ──────────────────────────────────────────────────────────────
function openApplyModal(role){
    document.getElementById('applyModalTitle').textContent = role;
    document.getElementById('modalRoleField').value = role;
    document.getElementById('modalSubjectField').value = 'New Application: ' + role;
    document.getElementById('applyModalOverlay').classList.add('open');
    document.body.style.overflow = 'hidden';
    // reset form state
    var form = document.getElementById('applyModalForm');
    var success = document.getElementById('modalFormSuccess');
    var status = document.getElementById('modalFormStatus');
    form.style.display = '';
    success.style.display = 'none';
    status.className = 'form-status';
    status.textContent = '';
    form.reset();
    document.getElementById('modalRoleField').value = role;
    document.getElementById('modalSubjectField').value = 'New Application: ' + role;
}
function closeApplyModal(){
    document.getElementById('applyModalOverlay').classList.remove('open');
    document.body.style.overflow = '';
}
document.getElementById('applyModalOverlay').addEventListener('click', function(e){
    if(e.target === this) closeApplyModal();
});
document.addEventListener('keydown', function(e){
    if(e.key === 'Escape') closeApplyModal();
});

document.getElementById('applyModalForm').addEventListener('submit', async function(e){
    e.preventDefault();
    var form = this;
    var status = document.getElementById('modalFormStatus');
    var success = document.getElementById('modalFormSuccess');
    var btn = document.getElementById('modalSubmitBtn');
    var role = document.getElementById('modalRoleField').value;
    btn.disabled = true;
    status.className = 'form-status visible';
    status.textContent = 'Sending\u2026';
    var formData = new FormData(form);
    try {
        var res = await fetch('https://api.web3forms.com/submit', {method:'POST', body:formData});
        var data = await res.json();
        if(data.success){
            form.style.display = 'none';
            status.className = 'form-status';
            document.getElementById('modalSuccessRole').textContent = role;
            success.style.display = 'block';
        } else {
            status.className = 'form-status visible error';
            status.textContent = data.message || 'Something went wrong. Please try again or email info@w13uk.com.';
            btn.disabled = false;
        }
    } catch(err){
        status.className = 'form-status visible error';
        status.textContent = 'Network error. Please try again or email info@w13uk.com.';
        btn.disabled = false;
    }
});

// ── General interest form (still on page) ───────────────────────────────────
var gf = document.getElementById('careersForm');
if(gf) gf.addEventListener('submit', async function(e){
    e.preventDefault();
    var form = this;
    var status = document.getElementById('formStatus');
    var success = document.getElementById('formSuccess');
    status.className = 'form-status visible';
    status.textContent = 'Sending\u2026';
    var formData = new FormData(form);
    try {
        var res = await fetch('https://api.web3forms.com/submit', {method:'POST', body:formData});
        var data = await res.json();
        if(data.success){
            form.style.display = 'none';
            status.classList.remove('visible');
            success.classList.add('visible');
            success.scrollIntoView({behavior:'smooth', block:'center'});
        } else {
            status.className = 'form-status visible error';
            status.textContent = data.message || 'Something went wrong. Please try again or email info@w13uk.com.';
        }
    } catch(err){
        status.className = 'form-status visible error';
        status.textContent = 'Network error. Please try again or email info@w13uk.com.';
    }
});
</script>'''

assert OLD_JS in html, 'OLD_JS block not found'
html = html.replace(OLD_JS, NEW_JS, 1)

# ── 5. WRITE ──────────────────────────────────────────────────────────────────
p.write_text(html)
print(f'Done. careers.html is now {len(html)} bytes.')
