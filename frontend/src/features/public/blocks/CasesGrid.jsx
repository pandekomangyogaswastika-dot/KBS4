import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";
import { PlanetOrb } from "@/components/decor";
import { useContentLocale } from "@/lib/useContentLocale";
import { GlassCard } from "@/components/kti/GlassCard";
import { fadeUp, stagger, viewportOnce } from "@/lib/motion";

export default function CasesGrid({ items = [] }) {
  const { L } = useContentLocale();
  return (
    <motion.div
      variants={stagger}
      initial="hidden"
      whileInView="show"
      viewport={viewportOnce}
      className="grid grid-cols-1 gap-6 md:grid-cols-2"
      data-testid="cases-grid"
    >
      {items.map((c) => (
        <motion.div key={c.id || c.slug} variants={fadeUp} className="h-full">
          <GlassCard
            as={Link}
            to={`/cases/${c.slug}`}
            tilt
            data-cursor="hover"
            data-testid={`case-card-${c.slug}`}
            className="flex h-full gap-5 p-6"
          >
            <div className="shrink-0 pt-1">
              {c.cover_image_url ? (
                <img src={c.cover_image_url} alt={L(c.title)} className="size-[84px] rounded-2xl object-cover ring-1 ring-white/12" loading="lazy" decoding="async" />
              ) : (
                <PlanetOrb variant={c.cover || "planet-indigo"} size={84} />
              )}
            </div>
            <div className="min-w-0">
              <span className="font-hud text-[11px] uppercase tracking-[0.22em]" style={{ color: "var(--kti-teal)" }}>
                {L(c.industry)}
              </span>
              <h3 className="mt-2 font-display text-lg font-semibold leading-snug">{L(c.title)}</h3>
              <p className="mt-2 line-clamp-3 text-sm leading-relaxed text-[color:var(--kti-text-dim)]">{L(c.summary)}</p>
              <span className="mt-4 inline-flex items-center gap-1 text-sm font-medium" style={{ color: "#cdd3ff" }}>
                {c.client_name}
                <ArrowUpRight className="size-4" />
              </span>
            </div>
          </GlassCard>
        </motion.div>
      ))}
    </motion.div>
  );
}
