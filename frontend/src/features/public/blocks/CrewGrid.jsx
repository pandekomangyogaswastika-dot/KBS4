import { motion } from "framer-motion";
import { CrewAvatar } from "@/components/decor";
import { useContentLocale } from "@/lib/useContentLocale";
import { GlassCard } from "@/components/kti/GlassCard";
import { fadeUp, stagger, viewportOnce } from "@/lib/motion";

export default function CrewGrid({ items = [] }) {
  const { L } = useContentLocale();
  return (
    <motion.div
      variants={stagger}
      initial="hidden"
      whileInView="show"
      viewport={viewportOnce}
      className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4"
      data-testid="crew-grid"
    >
      {items.map((m) => (
        <motion.div key={m.id} variants={fadeUp} className="h-full">
          <GlassCard data-testid={`crew-card-${m.id}`} className="h-full p-6 text-center">
            <div className="mx-auto w-fit">
              {m.avatar_url ? (
                <img src={m.avatar_url} alt={m.name} className="size-24 rounded-full object-cover ring-2 ring-white/15" loading="lazy" decoding="async" />
              ) : (
                <CrewAvatar name={m.name} seed={m.seed} size={96} />
              )}
            </div>
            <h3 className="mt-4 font-display text-base font-semibold">{m.name}</h3>
            <p className="mt-1 text-sm" style={{ color: "var(--kti-teal)" }}>{L(m.role)}</p>
            <p className="mt-3 text-xs leading-relaxed text-[color:var(--kti-text-dim)]">{L(m.bio)}</p>
          </GlassCard>
        </motion.div>
      ))}
    </motion.div>
  );
}
