{
  "design_system_name": "Kubus Teknologi Indonesia — V2 Cosmic Cinematic Glass",
  "version": "2.0",
  "brand_attributes": [
    "cinematic",
    "premium",
    "technical/HUD",
    "trustworthy enterprise",
    "space-cosmic",
    "glassmorphic",
    "scroll-storytelling"
  ],
  "global_rules": {
    "theme": "Default dark theme only. No light theme variants in V2.",
    "contrast": "All text must meet WCAG AA against near-black/video backdrops. Use overlays to guarantee legibility.",
    "bilingual": "Layouts must tolerate ID/EN length variance (±35%). Avoid fixed widths for nav items and CTAs.",
    "gradients": {
      "restriction": "Use gradients only as large background accents/overlays (<=20% viewport). Never on text-heavy reading areas or small UI elements (<100px). Never stack multiple gradients in same viewport.",
      "allowed": [
        "hero/section background overlays",
        "decorative aurora glows behind media",
        "large CTA background only (subtle)"
      ]
    },
    "testing": "All interactive and key informational elements MUST include data-testid (kebab-case, role-based).",
    "file_convention": "Project uses .js (not .tsx). Provide JS scaffolds only."
  },
  "inspiration_refs": {
    "ux_reference": {
      "name": "oryzo.ai (cinematic scroll storytelling)",
      "notes": [
        "ScrollTrigger pin + scrub timelines",
        "WebGL accents",
        "cinematic pacing + crossfades"
      ],
      "sources": [
        "https://www.cssdesignawards.com/wotm/oryzo-ai/49111/",
        "https://www.awwwards.com/sites/oryzo-ai",
        "https://gsap.com/docs/v3/Plugins/ScrollTrigger/"
      ]
    },
    "ui_language": {
      "pill_nav": "Floating glass capsule nav (centered links + right CTA)",
      "hud_motif": "Annotation connector lines + dots + mono labels",
      "two_tone_headlines": "Same-line emphasis: strong white keywords + dim gray supporting words"
    }
  },
  "typography": {
    "font_loading": {
      "google_fonts": [
        "Space Grotesk (already imported)",
        "Figtree (already imported)",
        "IBM Plex Mono (already imported)"
      ],
      "recommendation": {
        "display": {
          "name": "Space Grotesk",
          "why": "Geometric, modern, tech-forward; already in index.css so no new dependency risk. Use weight 600–700 with tighter tracking for cinematic headlines."
        },
        "body": {
          "name": "Figtree",
          "why": "High readability for bilingual paragraphs; friendly but still modern."
        },
        "mono": {
          "name": "IBM Plex Mono",
          "why": "HUD/annotation labels, metrics, tags, connector callouts."
        }
      }
    },
    "type_scale_px": {
      "hero_display": { "fontSize": 64, "lineHeight": 1.02, "letterSpacing": "-0.04em", "weight": 700 },
      "h1": { "fontSize": 48, "lineHeight": 1.08, "letterSpacing": "-0.03em", "weight": 700 },
      "h2": { "fontSize": 32, "lineHeight": 1.15, "letterSpacing": "-0.02em", "weight": 650 },
      "h3": { "fontSize": 22, "lineHeight": 1.25, "letterSpacing": "-0.01em", "weight": 650 },
      "body": { "fontSize": 16, "lineHeight": 1.65, "letterSpacing": "-0.005em", "weight": 450 },
      "small": { "fontSize": 13, "lineHeight": 1.55, "letterSpacing": "0.01em", "weight": 450 },
      "caption_mono": { "fontSize": 12, "lineHeight": 1.4, "letterSpacing": "0.22em", "weight": 500 }
    },
    "tailwind_mapping": {
      "hero_display": "text-4xl sm:text-5xl lg:text-6xl tracking-[-0.04em] leading-[1.02] font-bold",
      "h1": "text-4xl sm:text-5xl tracking-[-0.03em] leading-[1.08] font-bold",
      "h2": "text-2xl sm:text-3xl tracking-[-0.02em] leading-[1.15] font-semibold",
      "h3": "text-xl sm:text-[22px] tracking-[-0.01em] leading-[1.25] font-semibold",
      "body": "text-sm sm:text-base leading-relaxed text-[color:var(--kti-text-strong)]",
      "dim": "text-sm sm:text-base leading-relaxed text-[color:var(--kti-text-dim)]",
      "eyebrow": "font-mono-kti text-xs uppercase tracking-[0.35em] text-[color:var(--kti-teal)]"
    },
    "two_tone_headline_spec": {
      "pattern": "Wrap emphasis words in <span className=\"text-[color:var(--kti-text-strong)]\"> and supporting words in <span className=\"text-[color:var(--kti-text-dim)]\"> within the same heading.",
      "example_jsx": "<h1 className=\"font-display text-4xl sm:text-5xl lg:text-6xl tracking-[-0.04em] leading-[1.02]\"><span className=\"text-[color:var(--kti-text-strong)]\">Build</span> <span className=\"text-[color:var(--kti-text-dim)]\">mission-ready</span> <span className=\"text-[color:var(--kti-text-strong)]\">systems</span></h1>"
    }
  },
  "color_tokens": {
    "notes": "Keep Kubus brand purple/indigo/teal accents; cinematic near-black base; glass surfaces; controlled glows.",
    "css_variables_to_define_in_index_css": {
      "base": {
        "--kti-space-975": "#03040A",
        "--kti-space-950": "#05060A",
        "--kti-space-925": "#06070F",
        "--kti-space-900": "#0B0D17",
        "--kti-space-850": "#141728",
        "--kti-text-strong": "#E8EAF2",
        "--kti-text-dim": "#9AA0B5",
        "--kti-text-faint": "#6E748A"
      },
      "brand": {
        "--kti-purple": "#4F3E97",
        "--kti-indigo": "#7C68E1",
        "--kti-teal": "#73D1AD",
        "--kti-electric": "#B7A8FF"
      },
      "glass_surfaces": {
        "--kti-glass-bg": "rgba(255,255,255,0.06)",
        "--kti-glass-bg-strong": "rgba(255,255,255,0.09)",
        "--kti-glass-border": "rgba(255,255,255,0.12)",
        "--kti-glass-border-strong": "rgba(255,255,255,0.18)",
        "--kti-glass-inner-highlight": "rgba(255,255,255,0.10)",
        "--kti-glass-shadow": "0 18px 60px rgba(0,0,0,0.55)",
        "--kti-glass-shadow-hover": "0 26px 80px rgba(0,0,0,0.62)"
      },
      "glow_and_rings": {
        "--kti-ring": "rgba(124, 104, 225, 0.55)",
        "--kti-glow-indigo": "0 0 0 1px rgba(124,104,225,0.18), 0 0 40px rgba(124,104,225,0.18)",
        "--kti-glow-teal": "0 0 0 1px rgba(115,209,173,0.16), 0 0 44px rgba(115,209,173,0.14)",
        "--kti-glow-mix": "0 0 0 1px rgba(255,255,255,0.10), 0 0 60px rgba(124,104,225,0.14), 0 0 70px rgba(115,209,173,0.10)"
      },
      "overlays_for_media_legibility": {
        "--kti-media-overlay-top": "linear-gradient(180deg, rgba(5,6,10,0.78) 0%, rgba(5,6,10,0.35) 45%, rgba(5,6,10,0.82) 100%)",
        "--kti-media-overlay-side": "linear-gradient(90deg, rgba(5,6,10,0.78) 0%, rgba(5,6,10,0.25) 55%, rgba(5,6,10,0.78) 100%)",
        "--kti-aurora-accent": "radial-gradient(60% 60% at 20% 20%, rgba(124,104,225,0.22) 0%, rgba(124,104,225,0.0) 60%), radial-gradient(55% 55% at 80% 30%, rgba(115,209,173,0.18) 0%, rgba(115,209,173,0.0) 62%)"
      },
      "state_colors": {
        "--kti-success": "#73D1AD",
        "--kti-warning": "#F2C879",
        "--kti-danger": "#FF5C7A",
        "--kti-info": "#7C68E1"
      },
      "radius_and_spacing": {
        "--radius": "0.875rem",
        "--kti-radius-pill": "999px",
        "--kti-radius-card": "20px",
        "--kti-radius-soft": "14px"
      }
    },
    "tailwind_usage_examples": {
      "page_bg": "bg-[color:var(--kti-space-950)] text-[color:var(--kti-text-strong)]",
      "glass": "bg-[color:var(--kti-glass-bg)] border border-white/10 backdrop-blur-md",
      "glass_strong": "bg-[color:var(--kti-glass-bg-strong)] border border-white/15 backdrop-blur-xl",
      "media_overlay": "bg-[image:var(--kti-media-overlay-top)]"
    }
  },
  "layout_and_grid": {
    "container": "Use existing .kti-container utility (max-w-6xl). For hero/cinematic sections, allow full-bleed media with inner container overlay.",
    "grid": {
      "desktop": "12-col mental model; implement with Tailwind grid-cols-12 and gap-6/8.",
      "mobile": "Single column; avoid dense multi-column overlays on video. Use stacked content with generous padding.",
      "section_spacing": "Use .kti-section (py-16 sm:py-20 lg:py-28). Increase whitespace; never cramped."
    },
    "dividers": "Use thin vertical/horizontal dividers (Separator) with white/10 and occasional teal dot endpoints for HUD feel."
  },
  "component_path": {
    "shadcn_primary": [
      "/app/frontend/src/components/ui/button.jsx",
      "/app/frontend/src/components/ui/badge.jsx",
      "/app/frontend/src/components/ui/card.jsx",
      "/app/frontend/src/components/ui/navigation-menu.jsx",
      "/app/frontend/src/components/ui/sheet.jsx",
      "/app/frontend/src/components/ui/separator.jsx",
      "/app/frontend/src/components/ui/carousel.jsx",
      "/app/frontend/src/components/ui/accordion.jsx",
      "/app/frontend/src/components/ui/tabs.jsx",
      "/app/frontend/src/components/ui/tooltip.jsx",
      "/app/frontend/src/components/ui/sonner.jsx"
    ],
    "custom_components_to_create": [
      "src/components/kti/FloatingPillNavbar.js",
      "src/components/kti/GlassCard.js",
      "src/components/kti/GlassPillButton.js",
      "src/components/kti/DotBadge.js",
      "src/components/kti/AnnotationLine.js",
      "src/components/kti/MediaSection.js",
      "src/components/kti/ScrollScrubHero.js",
      "src/components/kti/HorizontalCasesRail.js",
      "src/components/kti/StickyStackServices.js",
      "src/components/kti/TwoToneHeading.js",
      "src/components/kti/StatsCountUp.js",
      "src/components/kti/CustomCursor.js"
    ]
  },
  "navbar_v2": {
    "goal": "Replace standard top bar with modern floating glass capsule nav.",
    "anatomy": {
      "wrapper": "Fixed top with safe-area padding; centered capsule; subtle blur; border; glow.",
      "left": "Kubus hex-K emblem + wordmark (click to top).",
      "center": "Nav links (Home, About, Services, Tech, Cases, Team, Contact). Active route uses pill highlight + dot.",
      "right": "Language toggle (ID/EN) + primary CTA pill button (e.g., 'Consultation').",
      "mobile": "Hamburger opens Sheet with same links + CTA + language toggle; capsule remains but simplified (logo + menu + CTA icon)."
    },
    "states": {
      "default": "Transparent-ish glass (bg white/5) over hero media.",
      "scrolled": "Increase blur + slightly darker tint; add subtle shadow; reduce height by ~6px.",
      "active_link": "Inner pill highlight: bg-white/8 + border-white/15 + tiny teal dot left.",
      "hover": "Link text brightens; underline becomes a 1px gradient line (indigo->teal) limited to link width.",
      "focus": "Use .kti-focus ring with --kti-ring."
    },
    "tailwind_recipe": {
      "capsule": "fixed top-4 left-1/2 -translate-x-1/2 z-50 w-[min(1100px,calc(100vw-1.5rem))] rounded-full bg-white/5 border border-white/10 backdrop-blur-xl shadow-[0_18px_60px_rgba(0,0,0,0.55)]",
      "inner": "flex items-center justify-between gap-3 px-3 sm:px-4 py-2",
      "link": "px-3 py-2 rounded-full text-sm text-[color:var(--kti-text-dim)] hover:text-[color:var(--kti-text-strong)]",
      "cta": "rounded-full bg-white/8 border border-white/14 hover:bg-white/10"
    },
    "data_testids": {
      "nav": "floating-pill-navbar",
      "lang_toggle": "navbar-language-toggle",
      "cta": "navbar-primary-cta-button",
      "mobile_menu": "navbar-mobile-menu-button"
    }
  },
  "card_system_v2": {
    "problem_to_fix": "V1 cards are flat dark rectangles. Replace with premium glassmorphic surfaces + depth + hover lift/tilt.",
    "base_glass_card": {
      "visual": [
        "bg: rgba(255,255,255,0.06)",
        "border: 1px solid rgba(255,255,255,0.12)",
        "backdrop-blur: 14–22px",
        "inner highlight: top inset line",
        "outer shadow: deep cinematic",
        "optional glow: indigo/teal very subtle"
      ],
      "hover": [
        "translateY(-4px)",
        "shadow increases",
        "border brightens to white/18",
        "optional: slight 3D tilt on pointer-fine devices only"
      ],
      "tailwind": "rounded-[var(--kti-radius-card)] bg-white/5 border border-white/10 backdrop-blur-xl shadow-[0_18px_60px_rgba(0,0,0,0.55)] hover:shadow-[0_26px_80px_rgba(0,0,0,0.62)]"
    },
    "annotation_connector_motif": {
      "spec": "Use 1px lines (white/12) with small endpoint dots (teal/70). Lines connect a mono label to a card corner or media focal point.",
      "implementation_hint": "Use absolutely positioned divs or SVG. Keep it decorative; do not block pointer events.",
      "tailwind": {
        "line": "absolute h-px bg-white/12",
        "dot": "absolute size-1.5 rounded-full bg-[color:var(--kti-teal)]/80 shadow-[0_0_0_3px_rgba(115,209,173,0.12)]"
      }
    },
    "pill_tags_with_dot": {
      "spec": "Badge-like pill with leading dot indicator. Use mono label for technical vibe.",
      "tailwind": "inline-flex items-center gap-2 rounded-full bg-white/6 border border-white/10 px-3 py-1 text-xs font-mono-kti uppercase tracking-[0.22em] text-[color:var(--kti-text-strong)]",
      "dot": "size-1.5 rounded-full bg-[color:var(--kti-teal)]"
    },
    "glass_pill_buttons": {
      "spec": "Primary CTA is a glass pill with a circular icon well on the right (arrow).",
      "anatomy": [
        "Left: label",
        "Right: circular icon container (bg white/10, border white/15)",
        "Hover: subtle glow + icon nudges 2px"
      ],
      "tailwind": {
        "button": "group inline-flex items-center justify-between gap-3 rounded-full bg-white/8 border border-white/14 px-5 py-3 text-sm font-semibold text-[color:var(--kti-text-strong)] shadow-[0_14px_40px_rgba(0,0,0,0.45)] hover:bg-white/10 focus-visible:ring-2 focus-visible:ring-[color:var(--kti-ring)]",
        "iconWell": "grid place-items-center size-9 rounded-full bg-white/10 border border-white/15 transition-colors",
        "icon": "transition-transform duration-200 group-hover:translate-x-0.5"
      },
      "data_testids": {
        "primary": "glass-pill-primary-button",
        "secondary": "glass-pill-secondary-button"
      }
    },
    "glass_data_stat_card": {
      "spec": "Small glass card with big stat + mini chart (Recharts) + mono label.",
      "layout": "Top row: label + delta badge; Middle: big number; Bottom: sparkline.",
      "recommended_lib": "recharts",
      "empty_state": "If no data, show Skeleton + 'Telemetry unavailable' caption."
    }
  },
  "cinematic_media_backgrounds": {
    "rule": "Every section uses full-bleed video/image background with overlays for legibility. Content sits in glass surfaces or on overlay columns.",
    "media_section_pattern": {
      "layers": [
        "Background media (video or image)",
        "Overlay gradient (top/bottom) using --kti-media-overlay-top",
        "Optional aurora accent (radial) using --kti-aurora-accent (<=20% viewport)",
        "Foreground content container"
      ],
      "tailwind": {
        "section": "relative min-h-[70vh] overflow-hidden",
        "media": "absolute inset-0 h-full w-full object-cover",
        "overlay": "absolute inset-0 bg-[image:var(--kti-media-overlay-top)]",
        "content": "relative z-10 kti-container"
      }
    },
    "hero_scroll_scrubbed_video": {
      "spec": {
        "pin": "Hero pinned for 120–180vh scroll distance.",
        "scrub": "Scroll progress drives video currentTime (desktop).",
        "content": "Headline + subcopy parallax slightly slower than video; CTA appears after 15% progress.",
        "poster": "Always provide poster image for first paint + reduced motion.",
        "mobile_fallback": "On mobile/low-power: no scrubbing; use poster image + subtle fade crossfade to next section.",
        "reduced_motion": "prefers-reduced-motion: pause video, show poster, disable pin/scrub; keep content static."
      },
      "implementation_notes_js": {
        "video_scrub": "Use requestAnimationFrame to set video.currentTime = progress * duration. Guard for metadata loaded.",
        "ScrollTrigger": "Create a timeline with ScrollTrigger { pin:true, scrub:true, start:'top top', end:'+=160%' }. Update video time in onUpdate.",
        "performance": "Use muted, playsInline, preload='auto'. Consider 720p for desktop; 480p for mobile."
      },
      "data_testids": {
        "hero": "hero-scroll-scrub-section",
        "hero_cta": "hero-primary-cta-button"
      }
    }
  },
  "motion_choreography": {
    "libraries": {
      "required": [
        "gsap",
        "gsap/ScrollTrigger",
        "@studio-freight/lenis",
        "framer-motion"
      ],
      "notes": "Use GSAP for scroll choreography; Framer Motion for component-level micro-interactions (hover/press) where GSAP is overkill."
    },
    "lenis_scrolltrigger_integration": {
      "pattern": "Use Lenis for smooth scroll and wire ScrollTrigger via scrollerProxy if using a custom scroll container. Always call ScrollTrigger.update on Lenis scroll.",
      "reference": "https://gsap.com/docs/v3/Plugins/ScrollTrigger/"
    },
    "gsap_specs": {
      "pinned_hero_video_scrub": {
        "trigger": "#hero",
        "start": "top top",
        "end": "+=160%",
        "pin": true,
        "scrub": 1,
        "onUpdate": "map progress to video.currentTime",
        "extras": [
          "headline y: 0 -> -24 (parallax)",
          "cta opacity 0 -> 1 at progress 0.15"
        ]
      },
      "section_crossfades": {
        "pattern": "As each section enters, crossfade overlay intensity and slightly scale media (1.02 -> 1.0).",
        "start": "top 80%",
        "end": "top 20%",
        "scrub": true
      },
      "line_by_line_text_reveal": {
        "pattern": "Split lines (manual spans) and animate y: 18->0, opacity:0->1 stagger 0.06.",
        "start": "top 78%",
        "toggleActions": "play none none reverse"
      },
      "sticky_stacking_services": {
        "pattern": "Service cards stack with sticky container; each card pins briefly and scales down previous card (1 -> 0.96) with blur increase.",
        "start": "top top",
        "end": "+=220%",
        "scrub": 1
      },
      "horizontal_cases": {
        "pattern": "Pinned horizontal rail; vertical scroll drives x translation of track.",
        "start": "top top",
        "end": "+=scrollDistance",
        "pin": true,
        "scrub": 1,
        "reference": "https://gsap.com/docs/v3/Plugins/ScrollTrigger/"
      },
      "count_up_stats": {
        "pattern": "On enter, animate numbers from 0 to target over 1.2s with easeOut; trigger once.",
        "start": "top 85%",
        "once": true
      },
      "magnetic_hover": {
        "pattern": "Pointer-fine only: CTA buttons slightly translate toward cursor within 6–10px radius; reset on leave.",
        "reduced_motion": "Disable magnetic effect."
      },
      "custom_cursor": {
        "pattern": "Use existing CSS cursor classes in index.css. Activate only on pointer-fine devices; enlarge ring on hover of links/buttons.",
        "reduced_motion": "Cursor can remain; no animation beyond size transition."
      }
    },
    "reduced_motion_policy": {
      "detect": "window.matchMedia('(prefers-reduced-motion: reduce)')",
      "behavior": [
        "Disable ScrollTrigger pin/scrub timelines",
        "Disable parallax and horizontal scroll",
        "Use simple fade-in (no translate) for reveals",
        "Use poster images instead of autoplay/scrub video"
      ]
    }
  },
  "section_blueprints": {
    "hero": {
      "layout": "Full-bleed scrubbed video with overlay; left column headline; right column glass telemetry card + annotation lines.",
      "components": [
        "ScrollScrubHero",
        "GlassPillButton",
        "DotBadge",
        "AnnotationLine",
        "GlassCard (telemetry)"
      ],
      "micro_interactions": [
        "CTA icon nudges on hover",
        "Telemetry card subtle float (disable reduced motion)"
      ]
    },
    "about": {
      "layout": "Cinematic image background; two-column: narrative + timeline/values cards; vertical divider line.",
      "components": [
        "TwoToneHeading",
        "GlassCard",
        "Separator",
        "Badge (dot pill)"
      ]
    },
    "services": {
      "layout": "Sticky stacking glass cards over slow parallax nebula background; each card has icon, title, bullets, CTA.",
      "components": [
        "StickyStackServices",
        "GlassCard",
        "Accordion (mobile details)",
        "GlassPillButton"
      ]
    },
    "tech": {
      "layout": "HUD-style grid of capabilities; include mini charts and metrics; annotation lines to a subtle imperative Three.js hex-crystal accent.",
      "components": [
        "GlassDataStatCard",
        "Tabs (platform/stack/security)",
        "Tooltip",
        "AnnotationLine"
      ],
      "3d": "Imperative Three.js hex-crystal accent only (small, decorative)."
    },
    "cases": {
      "layout": "Pinned horizontal rail of case cards with full-bleed thumbnails; each card opens Dialog with details.",
      "components": [
        "HorizontalCasesRail",
        "Card",
        "Dialog",
        "Carousel (inside dialog)"
      ]
    },
    "team": {
      "layout": "Cinematic portrait/video background; glass avatar cards with scanline overlay; role + expertise tags.",
      "components": [
        "Avatar",
        "GlassCard",
        "Badge",
        "Tooltip"
      ]
    },
    "clients": {
      "layout": "Logo wall on glass strip; subtle marquee (optional) with reduced-motion fallback static grid.",
      "components": [
        "ScrollArea (if needed)",
        "Separator"
      ]
    },
    "blog_career_teasers": {
      "layout": "Two glass feature cards with background media; hover lift; CTA.",
      "components": [
        "GlassCard",
        "GlassPillButton"
      ]
    },
    "contact": {
      "layout": "Full-bleed starfield + overlay; left: contact info + map link; right: glass form.",
      "components": [
        "Input",
        "Textarea",
        "Button",
        "Sonner (toast)"
      ],
      "data_testids": {
        "form": "contact-form",
        "submit": "contact-form-submit-button",
        "email": "contact-form-email-input",
        "message": "contact-form-message-textarea"
      }
    }
  },
  "images_and_media": {
    "note": "Use royalty-free cinematic footage/imagery as placeholders. Replace with client-provided assets later.",
    "image_urls": [
      {
        "category": "cases/background",
        "description": "Abstract HUD / holographic tunnel background for tech sections (use as poster or subtle overlay).",
        "url": "https://images.unsplash.com/photo-1618130619951-8c8ec0eb23eb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MDZ8MHwxfHNlYXJjaHwzfHxhYnN0cmFjdCUyMGhvbG9ncmFwaGljJTIwaHVkJTIwaW50ZXJmYWNlJTIwbGluZXMlMjBkb3RzJTIwZGFya3xlbnwwfHx8Ymx1ZXwxNzgwMDU5NDcwfDA&ixlib=rb-4.1.0&q=85"
      },
      {
        "category": "hero/sky",
        "description": "Cinematic moon/sky placeholder (use as reduced-motion poster).",
        "url": "https://images.unsplash.com/photo-1585835074092-32639ccfe3ce?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA3MDR8MHwxfHNlYXJjaHwzfHxhc3Ryb25hdXQlMjBtb29uJTIwY2luZW1hdGljJTIwd2lkZSUyMHNob3R8ZW58MHx8fHRlYWx8MTc4MDA1OTQ3MHww&ixlib=rb-4.1.0&q=85"
      },
      {
        "category": "tech/abstract",
        "description": "Neon tech surface close-up (use as section background with strong overlay).",
        "url": "https://images.pexels.com/photos/7562103/pexels-photo-7562103.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
      }
    ],
    "video_placeholders": {
      "hero": "Use a royalty-free space/nebula cinematic clip (MP4/H.264). Provide poster JPG. Keep file size reasonable.",
      "sections": "Each section can use a short looping clip (6–10s) or a still image with subtle parallax."
    }
  },
  "implementation_scaffolds_js": {
    "two_tone_heading_component": {
      "file": "src/components/kti/TwoToneHeading.js",
      "api": "<TwoToneHeading as=\"h2\" strong=\"Mission-ready\" dim=\"systems for modern enterprises\" />",
      "notes": "Render strong + dim spans; keep semantics via 'as' prop."
    },
    "scroll_scrub_hero_component": {
      "file": "src/components/kti/ScrollScrubHero.js",
      "notes": [
        "Use refs for video + section",
        "Wait for loadedmetadata",
        "Create ScrollTrigger pinned timeline",
        "OnUpdate set video.currentTime",
        "Fallback: if reduced motion or mobile, do not create ScrollTrigger; show poster"
      ]
    },
    "horizontal_cases_component": {
      "file": "src/components/kti/HorizontalCasesRail.js",
      "notes": [
        "Pinned section + translateX track",
        "Use invalidateOnRefresh",
        "Use containerAnimation for nested reveals if needed"
      ]
    }
  },
  "instructions_to_main_agent": [
    "Update /app/frontend/src/index.css tokens to match the expanded token list (keep existing ones; add missing).",
    "Implement FloatingPillNavbar first (highest client pain). Ensure data-testid on nav, links, CTA, language toggle.",
    "Replace all flat cards with GlassCard system (backdrop blur + inner highlight + hover lift).",
    "Implement ScrollScrubHero with GSAP ScrollTrigger pin+scrub; add reduced-motion + mobile fallback.",
    "Apply MediaSection pattern to ALL sections: full-bleed media + overlay + content container.",
    "Add cinematic scroll choreography: sticky stacking Services, horizontal Cases, line reveals, count-up stats, crossfades.",
    "Do not use gradients beyond overlays/accent glows; keep within 20% viewport.",
    "Ensure every interactive element and key info has data-testid (kebab-case).",
    "Prefer shadcn/ui primitives for UI controls; avoid raw HTML dropdowns/toasts/etc."
  ],
  "general_ui_ux_design_guidelines_appendix": "<General UI UX Design Guidelines>\n    - You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms\n    - You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text\n   - NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json\n\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. \n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals.\n</General UI UX Design Guidelines>"
}
