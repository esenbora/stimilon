import Link from "next/link";
import { Button } from "../components/ui";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-[var(--background)]/80 backdrop-blur-sm border-b border-[var(--border)] z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-[var(--color-accent)] rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">S</span>
            </div>
            <span className="font-semibold text-lg">Stimilon</span>
          </div>
          <div className="flex items-center gap-4">
            <Link
              href="#features"
              className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
            >
              Features
            </Link>
            <Link
              href="#pricing"
              className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
            >
              Pricing
            </Link>
            <Link href="/dashboard">
              <Button size="sm">Start Scanning</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-[var(--muted)] rounded-full text-sm mb-6">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            Now in Beta
          </div>

          <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
            Penetration Testing
            <br />
            <span className="text-[var(--color-accent)]">for LLM Applications</span>
          </h1>

          <p className="text-xl text-[var(--muted-foreground)] mb-8 max-w-2xl mx-auto">
            Automated security testing that finds prompt injections, jailbreaks,
            and data leakage vulnerabilities in your AI applications before
            attackers do.
          </p>

          <div className="flex items-center justify-center gap-4">
            <Link href="/dashboard">
              <Button size="lg">Start Free Scan</Button>
            </Link>
            <Link href="#demo">
              <Button variant="secondary" size="lg">
                Watch Demo
              </Button>
            </Link>
          </div>

          <p className="text-sm text-[var(--muted-foreground)] mt-4">
            No credit card required. 10 free scans per day.
          </p>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 border-y border-[var(--border)] bg-[var(--muted)]/30">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-[var(--color-accent)]">23+</div>
              <div className="text-sm text-[var(--muted-foreground)]">Attack Tests</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-[var(--color-accent)]">2</div>
              <div className="text-sm text-[var(--muted-foreground)]">LLM Providers</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-[var(--color-accent)]">3</div>
              <div className="text-sm text-[var(--muted-foreground)]">Attack Categories</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-[var(--color-accent)]">&lt;5min</div>
              <div className="text-sm text-[var(--muted-foreground)]">Scan Time</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">
            Comprehensive LLM Security Testing
          </h2>
          <p className="text-center text-[var(--muted-foreground)] mb-12 max-w-2xl mx-auto">
            Our attack library covers the most common and dangerous LLM vulnerabilities
          </p>

          <div className="grid md:grid-cols-3 gap-6">
            {/* Prompt Injection */}
            <div className="p-6 border border-[var(--border)] rounded-xl">
              <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Prompt Injection</h3>
              <p className="text-[var(--muted-foreground)] text-sm mb-4">
                10 different injection techniques including instruction override,
                delimiter escape, and XML tag manipulation.
              </p>
              <ul className="text-sm space-y-1">
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-[var(--color-accent)] rounded-full" />
                  System prompt extraction
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-[var(--color-accent)] rounded-full" />
                  Context switching attacks
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-[var(--color-accent)] rounded-full" />
                  Unicode manipulation
                </li>
              </ul>
            </div>

            {/* Jailbreaks */}
            <div className="p-6 border border-[var(--border)] rounded-xl">
              <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Jailbreaks</h3>
              <p className="text-[var(--muted-foreground)] text-sm mb-4">
                8 jailbreak techniques testing safety guardrail bypasses
                including DAN, roleplay, and encoding attacks.
              </p>
              <ul className="text-sm space-y-1">
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-[var(--color-accent)] rounded-full" />
                  DAN (Do Anything Now)
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-[var(--color-accent)] rounded-full" />
                  Base64 encoding bypass
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-[var(--color-accent)] rounded-full" />
                  Emotional manipulation
                </li>
              </ul>
            </div>

            {/* Data Extraction */}
            <div className="p-6 border border-[var(--border)] rounded-xl">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Data Extraction</h3>
              <p className="text-[var(--muted-foreground)] text-sm mb-4">
                5 extraction probes testing for information leakage from
                system prompts, training data, and RAG systems.
              </p>
              <ul className="text-sm space-y-1">
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-[var(--color-accent)] rounded-full" />
                  Training data memorization
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-[var(--color-accent)] rounded-full" />
                  PII extraction attempts
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-[var(--color-accent)] rounded-full" />
                  RAG content exposure
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-[var(--muted)]/30">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to secure your LLM application?
          </h2>
          <p className="text-[var(--muted-foreground)] mb-8">
            Start with a free scan and get a comprehensive security report in minutes.
          </p>
          <Link href="/dashboard">
            <Button size="lg">Start Free Scan</Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-[var(--border)]">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-[var(--color-accent)] rounded flex items-center justify-center">
              <span className="text-white font-bold text-xs">S</span>
            </div>
            <span className="text-sm text-[var(--muted-foreground)]">
              Stimilon &copy; 2025
            </span>
          </div>
          <div className="flex items-center gap-4 text-sm text-[var(--muted-foreground)]">
            <Link href="/privacy" className="hover:text-[var(--foreground)]">
              Privacy
            </Link>
            <Link href="/terms" className="hover:text-[var(--foreground)]">
              Terms
            </Link>
            <a
              href="https://github.com/stimilon"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-[var(--foreground)]"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
