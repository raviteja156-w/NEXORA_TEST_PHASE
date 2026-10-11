/* ========================================================
   NEXORA — USER / SEEKER DASHBOARD INTERACTIONS
   Handles UI state, Supabase auth profile, and navigation
======================================================== */

document.addEventListener("DOMContentLoaded", () => {
  // Obtain Supabase client reference reliably
  const getSupabase = () => {
    return window.supabaseClient || (typeof supabaseClient !== "undefined" ? supabaseClient : null);
  };

  // Mobile sidebar toggle
  const mobileMenu = document.getElementById("mobileMenu");
  const sidebar = document.getElementById("sidebar");

  mobileMenu?.addEventListener("click", (e) => {
    e.stopPropagation();
    sidebar?.classList.toggle("open");
  });

  document.addEventListener("click", (e) => {
    if (sidebar && !sidebar.contains(e.target) && !mobileMenu?.contains(e.target)) {
      sidebar.classList.remove("open");
    }
  });

  // Banner close
  document.querySelector(".banner-close")?.addEventListener("click", (event) => {
    const banner = event.currentTarget.closest(".plan-banner");
    if (banner) {
      banner.style.display = "none";
    }
  });

  // Profile Dropdown Toggle
  const profileBtn = document.getElementById("profileBtn");
  const profileDropdown = document.getElementById("profileDropdown");

  profileBtn?.addEventListener("click", (e) => {
    e.stopPropagation();
    profileDropdown?.classList.toggle("show");
  });

  document.addEventListener("click", (e) => {
    if (profileDropdown && !profileDropdown.contains(e.target) && !profileBtn?.contains(e.target)) {
      profileDropdown.classList.remove("show");
    }
  });

  // Supabase Auth Integration — Load user profile
  const client = getSupabase();
  if (client) {
    client.auth.getSession().then(({ data: { session } }) => {
      if (session && session.user) {
        const user = session.user;
        const meta = user.user_metadata || {};
        const fullName = meta.full_name || meta.name || user.email?.split("@")[0] || "Job Seeker";
        const email = user.email || "";

        // Get initials
        const parts = fullName.trim().split(/\s+/);
        let initials = "JS";
        if (parts.length >= 2) {
          initials = (parts[0][0] + parts[1][0]).toUpperCase();
        } else if (parts.length === 1 && parts[0].length > 0) {
          initials = parts[0].substring(0, 2).toUpperCase();
        }

        // Update DOM elements
        const nameEl = document.getElementById("profileName");
        if (nameEl) nameEl.textContent = fullName;

        const dropdownNameEl = document.getElementById("dropdownUserName");
        if (dropdownNameEl) dropdownNameEl.textContent = fullName;

        const emailEl = document.getElementById("profileEmail");
        if (emailEl) emailEl.textContent = email;

        const avatarEl = document.getElementById("avatarInitials");
        if (avatarEl) avatarEl.textContent = initials;
      }
    });
  }

  // Unified Robust Logout Function
  const handleLogout = async (e) => {
    if (e) e.preventDefault();
    const btn = e ? e.currentTarget : null;
    if (btn) {
      btn.textContent = "Signing out...";
      btn.style.opacity = "0.7";
      btn.style.pointerEvents = "none";
    }

    const sb = getSupabase();
    if (sb) {
      try {
        await sb.auth.signOut();
      } catch (err) {
        console.error("Supabase signOut error:", err);
      }
    }

    // Force purge all Supabase session keys from localStorage
    try {
      Object.keys(localStorage).forEach((key) => {
        if (key.startsWith("sb-") || key.includes("supabase")) {
          localStorage.removeItem(key);
        }
      });
    } catch (err) {
      console.error("LocalStorage purge error:", err);
    }

    // Purge sessionStorage too just in case
    try {
      sessionStorage.clear();
    } catch (_) {}

    const appShell = document.getElementById("appShell");
    const homeUrl = appShell?.dataset?.homeUrl || "/";
    window.location.replace(homeUrl);
  };

  // Attach logout handler to all logout buttons
  document.querySelectorAll("#logoutBtn, #sidebarLogoutBtn, [data-action='logout']").forEach((btn) => {
    btn.addEventListener("click", handleLogout);
  });

  // Upgrade & Plan Buttons Navigation
  const appShell = document.getElementById("appShell");
  const plansUrl = appShell?.dataset?.plansUrl || "/auth/plans";
  document.querySelectorAll(".pink-btn, .blue-btn, .outline-green, [data-action='view-plans']").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = plansUrl;
    });
  });

  // View Job Buttons
  const jobsUrl = appShell?.dataset?.jobsUrl || "/jobs";
  document.querySelectorAll(".view-job").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      if (window.showToast) {
        window.showToast("Opening job details...", "info");
      }
      setTimeout(() => {
        window.location.href = jobsUrl;
      }, 400);
    });
  });
});
