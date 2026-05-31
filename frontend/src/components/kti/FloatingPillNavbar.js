import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Menu, Globe, ArrowRight } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger, SheetClose, SheetTitle } from "@/components/ui/sheet";
import { KubusMark } from "@/components/decor";
import { GlobalSearch } from "@/components/GlobalSearch";

const NAV = [
  ["services", "/services"],
  ["cases", "/cases"],
  ["tech", "/tech"],
  ["team", "/team"],
  ["blog", "/blog"],
  ["career", "/career"],
  ["contact", "/contact"],
];

const Dot = ({ active }) =>
  active ? (
    <span
      className="size-1.5 rounded-full"
      style={{ background: "var(--kti-teal)", boxShadow: "0 0 8px var(--kti-teal)" }}
    />
  ) : null;

export const FloatingPillNavbar = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const isEN = i18n.language && i18n.language.startsWith("en");
  const toggleLang = () => {
    const next = isEN ? "id" : "en";
    i18n.changeLanguage(next);
    localStorage.setItem("kti_locale", next);
  };

  const isActive = (path) => (path === "/" ? pathname === "/" : pathname.startsWith(path));

  const navCls = (active) =>
    `kti-focus relative inline-flex items-center gap-1.5 rounded-full px-3 py-2 text-[13px] transition-colors duration-200 ${
      active
        ? "bg-white/[0.08] text-white border border-white/[0.12]"
        : "text-[color:var(--kti-text-dim)] hover:text-white border border-transparent"
    }`;

  return (
    <header
      className="fixed inset-x-0 top-3 sm:top-4 flex justify-center px-3"
      style={{ zIndex: "var(--z-nav)" }}
    >
      <nav
        data-testid="floating-pill-navbar"
        className={`flex w-[min(1200px,100%)] items-center justify-between gap-2 rounded-full border px-2.5 py-2 backdrop-blur-xl transition-[background-color,border-color,box-shadow] duration-300 ${
          scrolled
            ? "border-white/[0.14] bg-[rgba(8,9,16,0.72)] shadow-[0_18px_60px_rgba(0,0,0,0.55)]"
            : "border-white/10 bg-white/[0.05]"
        }`}
      >
        <Link
          to="/"
          data-testid="nav-home-logo"
          aria-label="Kubus home"
          className="kti-focus flex shrink-0 items-center rounded-full px-2 py-1"
        >
          <KubusMark height={30} />
        </Link>

        <div className="hidden lg:flex items-center gap-0.5">
          <Link to="/services" data-testid="nav-services" className={navCls(isActive("/services"))}>
            <Dot active={isActive("/services")} />{t("nav.services")}
          </Link>
          <Link to="/cases" data-testid="nav-cases" className={navCls(isActive("/cases"))}>
            <Dot active={isActive("/cases")} />{t("nav.cases")}
          </Link>
          <Link to="/tech" data-testid="nav-tech" className={navCls(isActive("/tech"))}>
            <Dot active={isActive("/tech")} />{t("nav.tech")}
          </Link>
          <Link to="/team" data-testid="nav-team" className={navCls(isActive("/team"))}>
            <Dot active={isActive("/team")} />{t("nav.team")}
          </Link>
          <Link to="/blog" data-testid="nav-blog" className={navCls(isActive("/blog"))}>
            <Dot active={isActive("/blog")} />{t("nav.blog")}
          </Link>
          <Link to="/career" data-testid="nav-career" className={navCls(isActive("/career"))}>
            <Dot active={isActive("/career")} />{t("nav.career")}
          </Link>
          <Link to="/contact" data-testid="nav-contact" className={navCls(isActive("/contact"))}>
            <Dot active={isActive("/contact")} />{t("nav.contact")}
          </Link>
        </div>

        <div className="flex items-center gap-2">
          <GlobalSearch scope="public" className="hidden lg:inline-flex" />
          <button
            onClick={toggleLang}
            data-testid="navbar-language-toggle"
            aria-label="Toggle language"
            className="kti-focus flex items-center gap-1.5 rounded-full border border-white/10 px-3 py-2 text-xs font-medium text-[color:var(--kti-text-strong)] hover:bg-white/[0.06] transition-colors"
          >
            <Globe className="size-4" style={{ color: "var(--kti-teal)" }} />
            {isEN ? "EN" : "ID"}
          </button>

          <button
            onClick={() => navigate("/contact")}
            data-testid="navbar-primary-cta-button"
            className="kti-focus hidden sm:inline-flex items-center gap-2 rounded-full border border-[rgba(124,104,225,0.45)] bg-[rgba(124,104,225,0.18)] px-4 py-2 text-[13px] font-semibold text-white shadow-[var(--kti-glow-indigo)] transition-colors hover:bg-[rgba(124,104,225,0.28)]"
          >
            {t("nav.consultation")}
            <ArrowRight className="size-4" />
          </button>

          <Sheet>
            <SheetTrigger asChild>
              <button
                className="kti-focus lg:hidden grid size-10 place-items-center rounded-full border border-white/10 hover:bg-white/[0.06]"
                data-testid="navbar-mobile-menu-button"
                aria-label="Open menu"
              >
                <Menu className="size-5" />
              </button>
            </SheetTrigger>
            <SheetContent
              side="right"
              className="border-white/10"
              style={{ background: "#0B0D17", color: "#E8EAF2" }}
            >
              <SheetTitle className="sr-only">{t("nav.menu")}</SheetTitle>
              <div className="mt-10 flex flex-col gap-1">
                {NAV.map(([key, path]) => (
                  <SheetClose asChild key={key}>
                    <Link
                      to={path}
                      data-testid={`nav-mobile-${key}`}
                      className={`rounded-xl px-3 py-3 text-base transition-colors ${
                        isActive(path) ? "bg-white/[0.08] text-white" : "hover:bg-white/[0.06]"
                      }`}
                    >
                      {t(`nav.${key}`)}
                    </Link>
                  </SheetClose>
                ))}
                <SheetClose asChild>
                  <Link
                    to="/portal/login"
                    data-testid="nav-client-login"
                    className="mt-2 rounded-xl border border-white/10 px-3 py-3 text-base hover:bg-white/[0.06]"
                  >
                    {t("nav.clientLogin")}
                  </Link>
                </SheetClose>
                <SheetClose asChild>
                  <Link
                    to="/contact"
                    data-testid="nav-mobile-cta"
                    className="mt-1 inline-flex items-center justify-between rounded-xl border border-[rgba(124,104,225,0.45)] bg-[rgba(124,104,225,0.18)] px-4 py-3 text-base font-semibold text-white"
                  >
                    {t("nav.consultation")}
                    <ArrowRight className="size-4" />
                  </Link>
                </SheetClose>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </nav>
    </header>
  );
};
