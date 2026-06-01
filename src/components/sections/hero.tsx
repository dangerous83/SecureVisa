import {
  ShieldCheck,
  Lock,
  ArrowRight,
  CheckCircle2,
  Globe2,
  FileCheck2,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

const stats = [
  { value: "120+", label: "Countries supported" },
  { value: "98.7%", label: "Approval success rate" },
  { value: "256-bit", label: "End-to-end encryption" },
  { value: "24/7", label: "Compliance monitoring" },
]

const trustPoints = [
  "SOC 2 Type II certified",
  "GDPR & data-residency compliant",
  "Bank-grade document vault",
]

export function Hero() {
  return (
    <section className="relative overflow-hidden">
      {/* Decorative background */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 -z-10"
      >
        <div className="absolute left-1/2 top-[-12rem] h-[28rem] w-[44rem] -translate-x-1/2 rounded-full bg-primary/10 blur-3xl" />
        <div className="absolute right-[-8rem] top-32 h-72 w-72 rounded-full bg-cta/10 blur-3xl" />
      </div>

      {/* Nav */}
      <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
        <a href="#" className="flex items-center gap-2" aria-label="SecureVisa home">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <ShieldCheck className="size-5" />
          </span>
          <span className="text-lg font-extrabold tracking-tight text-foreground">
            Secure<span className="text-primary">Visa</span>
          </span>
        </a>

        <nav className="hidden items-center gap-8 text-sm font-medium text-muted-foreground md:flex">
          <a href="#" className="transition-colors hover:text-foreground">Solutions</a>
          <a href="#" className="transition-colors hover:text-foreground">Security</a>
          <a href="#" className="transition-colors hover:text-foreground">Pricing</a>
          <a href="#" className="transition-colors hover:text-foreground">Resources</a>
        </nav>

        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" className="hidden sm:inline-flex">
            Sign in
          </Button>
          <Button variant="cta" size="sm">
            Get a quote
            <ArrowRight />
          </Button>
        </div>
      </header>

      {/* Hero body */}
      <div className="mx-auto grid max-w-7xl items-center gap-12 px-6 pb-20 pt-10 lg:grid-cols-2 lg:pb-28 lg:pt-16">
        <div className="flex flex-col items-start text-left">
          <Badge variant="trust">
            <Lock />
            Trusted by global immigration teams
          </Badge>

          <h1 className="mt-6 text-4xl font-extrabold leading-[1.1] tracking-tight text-foreground sm:text-5xl lg:text-6xl">
            Visa processing,{" "}
            <span className="text-primary">secured end to end.</span>
          </h1>

          <p className="mt-6 max-w-xl text-lg leading-relaxed text-muted-foreground">
            SecureVisa unifies applications, document verification, and compliance
            into one encrypted platform — so your team moves faster while every
            applicant's data stays protected.
          </p>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Button variant="cta" size="lg">
              Start free assessment
              <ArrowRight />
            </Button>
            <Button variant="outline" size="lg">
              Talk to sales
            </Button>
          </div>

          <ul className="mt-8 flex flex-col gap-2.5 sm:flex-row sm:flex-wrap sm:gap-x-6">
            {trustPoints.map((point) => (
              <li
                key={point}
                className="flex items-center gap-2 text-sm font-medium text-muted-foreground"
              >
                <CheckCircle2 className="size-4 shrink-0 text-primary" />
                {point}
              </li>
            ))}
          </ul>
        </div>

        {/* Trust / proof card */}
        <div className="relative">
          <div className="rounded-2xl border border-border bg-card p-6 shadow-xl shadow-primary/5 sm:p-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <FileCheck2 className="size-6" />
                </span>
                <div>
                  <p className="text-sm font-semibold text-foreground">
                    Application #SV-48201
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Skilled Worker · United Kingdom
                  </p>
                </div>
              </div>
              <Badge variant="trust">
                <ShieldCheck />
                Verified
              </Badge>
            </div>

            <div className="mt-6 space-y-4">
              {[
                { label: "Identity verification", done: true },
                { label: "Document encryption", done: true },
                { label: "Compliance screening", done: true },
                { label: "Officer review", done: false },
              ].map((step) => (
                <div key={step.label} className="flex items-center gap-3">
                  <span
                    className={[
                      "flex h-6 w-6 items-center justify-center rounded-full",
                      step.done
                        ? "bg-primary text-primary-foreground"
                        : "border border-border bg-muted text-muted-foreground",
                    ].join(" ")}
                  >
                    {step.done ? (
                      <CheckCircle2 className="size-4" />
                    ) : (
                      <span className="size-2 rounded-full bg-current" />
                    )}
                  </span>
                  <span className="text-sm font-medium text-foreground">
                    {step.label}
                  </span>
                  <span className="ml-auto text-xs font-medium text-muted-foreground">
                    {step.done ? "Complete" : "In progress"}
                  </span>
                </div>
              ))}
            </div>

            <div className="mt-6 flex items-center gap-2 rounded-lg bg-muted px-4 py-3 text-xs text-muted-foreground">
              <Globe2 className="size-4 shrink-0 text-primary" />
              Data stored in region · AES-256 at rest · TLS 1.3 in transit
            </div>
          </div>
        </div>
      </div>

      {/* Proof / stats strip */}
      <div className="border-t border-border bg-card/60">
        <dl className="mx-auto grid max-w-7xl grid-cols-2 gap-8 px-6 py-10 lg:grid-cols-4">
          {stats.map((stat) => (
            <div key={stat.label} className="text-left">
              <dt className="text-3xl font-extrabold tracking-tight text-foreground">
                {stat.value}
              </dt>
              <dd className="mt-1 text-sm text-muted-foreground">{stat.label}</dd>
            </div>
          ))}
        </dl>
      </div>
    </section>
  )
}
