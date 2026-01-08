"use client";

import { useState } from "react";
import Link from "next/link";
import { Button, Input, Card, CardHeader, CardTitle, CardContent } from "../../components/ui";

type Provider = "custom" | "openai" | "anthropic";
type RequestFormat = "simple" | "openai" | "anthropic";

interface ScanFormData {
  endpoint: string;
  apiKey: string;
  provider: Provider;
  requestFormat: RequestFormat;
  categories: string[];
  rateLimit: number;
}

export default function Dashboard() {
  const [formData, setFormData] = useState<ScanFormData>({
    endpoint: "",
    apiKey: "",
    provider: "custom",
    requestFormat: "simple",
    categories: ["injection", "jailbreak", "extraction"],
    rateLimit: 10,
  });
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleCategoryToggle = (category: string) => {
    setFormData((prev) => ({
      ...prev,
      categories: prev.categories.includes(category)
        ? prev.categories.filter((c) => c !== category)
        : [...prev.categories, category],
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsScanning(true);
    setScanResult(null);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/api/scans/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          endpoint: formData.endpoint,
          api_key: formData.apiKey || null,
          provider: formData.provider,
          request_format: formData.requestFormat,
          categories: formData.categories,
          rate_limit: formData.rateLimit,
        }),
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error(err || "Scan failed");
      }

      const result = await response.json();
      setScanResult(result);
    } catch (err: any) {
      console.error("Scan error:", err);
      setError(err.message || "Scan failed. Make sure the API server is running.");
    } finally {
      setIsScanning(false);
    }
  };

  const isCustomEndpoint = formData.provider === "custom";

  return (
    <div className="min-h-screen bg-[var(--muted)]/30">
      {/* Header */}
      <header className="bg-[var(--background)] border-b border-[var(--border)]">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-[var(--color-accent)] rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">S</span>
            </div>
            <span className="font-semibold text-lg">Stimilon</span>
          </Link>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-2">Security Scan</h1>
        <p className="text-[var(--muted-foreground)] mb-8">
          Test your chatbot or LLM application for security vulnerabilities
        </p>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Scan Form */}
          <div className="md:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Target Configuration</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Mode Selection */}
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      What do you want to test?
                    </label>
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() =>
                          setFormData((prev) => ({ ...prev, provider: "custom" }))
                        }
                        className={`flex-1 px-4 py-3 rounded-lg border text-sm font-medium transition-colors ${
                          formData.provider === "custom"
                            ? "bg-[var(--color-accent)] text-white border-[var(--color-accent)]"
                            : "border-[var(--border)] hover:border-[var(--color-accent)]"
                        }`}
                      >
                        <div className="font-semibold">My Chatbot</div>
                        <div className="text-xs opacity-80">Custom endpoint URL</div>
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          setFormData((prev) => ({ ...prev, provider: "openai" }))
                        }
                        className={`flex-1 px-4 py-3 rounded-lg border text-sm font-medium transition-colors ${
                          formData.provider === "openai"
                            ? "bg-[var(--color-accent)] text-white border-[var(--color-accent)]"
                            : "border-[var(--border)] hover:border-[var(--color-accent)]"
                        }`}
                      >
                        <div className="font-semibold">OpenAI</div>
                        <div className="text-xs opacity-80">Direct API test</div>
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          setFormData((prev) => ({ ...prev, provider: "anthropic" }))
                        }
                        className={`flex-1 px-4 py-3 rounded-lg border text-sm font-medium transition-colors ${
                          formData.provider === "anthropic"
                            ? "bg-[var(--color-accent)] text-white border-[var(--color-accent)]"
                            : "border-[var(--border)] hover:border-[var(--color-accent)]"
                        }`}
                      >
                        <div className="font-semibold">Anthropic</div>
                        <div className="text-xs opacity-80">Direct API test</div>
                      </button>
                    </div>
                  </div>

                  {/* Custom Endpoint URL */}
                  {isCustomEndpoint && (
                    <>
                      <Input
                        label="Your Chatbot URL"
                        type="url"
                        placeholder="https://api.yourcompany.com/chat"
                        value={formData.endpoint}
                        onChange={(e) =>
                          setFormData((prev) => ({ ...prev, endpoint: e.target.value }))
                        }
                        required
                      />

                      {/* Request Format */}
                      <div>
                        <label className="block text-sm font-medium mb-2">
                          Request Format
                        </label>
                        <div className="flex gap-2">
                          {[
                            { value: "simple", label: "Simple JSON", desc: '{"message": "..."}' },
                            { value: "openai", label: "OpenAI Format", desc: '{"messages": [...]}' },
                          ].map((fmt) => (
                            <button
                              key={fmt.value}
                              type="button"
                              onClick={() =>
                                setFormData((prev) => ({
                                  ...prev,
                                  requestFormat: fmt.value as RequestFormat,
                                }))
                              }
                              className={`flex-1 px-3 py-2 rounded-lg border text-sm transition-colors ${
                                formData.requestFormat === fmt.value
                                  ? "bg-[var(--color-accent)] text-white border-[var(--color-accent)]"
                                  : "border-[var(--border)] hover:border-[var(--color-accent)]"
                              }`}
                            >
                              <div className="font-medium">{fmt.label}</div>
                              <div className="text-xs opacity-70 font-mono">{fmt.desc}</div>
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Optional Auth Token */}
                      <Input
                        label="Auth Token (optional)"
                        type="password"
                        placeholder="Bearer token or API key"
                        value={formData.apiKey}
                        onChange={(e) =>
                          setFormData((prev) => ({ ...prev, apiKey: e.target.value }))
                        }
                      />
                    </>
                  )}

                  {/* Direct API - needs API key */}
                  {!isCustomEndpoint && (
                    <Input
                      label="API Key"
                      type="password"
                      placeholder={
                        formData.provider === "openai" ? "sk-..." : "sk-ant-..."
                      }
                      value={formData.apiKey}
                      onChange={(e) =>
                        setFormData((prev) => ({ ...prev, apiKey: e.target.value }))
                      }
                      required
                    />
                  )}

                  {/* Categories */}
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Attack Categories
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {[
                        { id: "injection", label: "Injection", count: 10 },
                        { id: "jailbreak", label: "Jailbreak", count: 8 },
                        { id: "extraction", label: "Extraction", count: 5 },
                      ].map((cat) => (
                        <button
                          key={cat.id}
                          type="button"
                          onClick={() => handleCategoryToggle(cat.id)}
                          className={`px-3 py-1.5 rounded-lg border text-sm font-medium transition-colors ${
                            formData.categories.includes(cat.id)
                              ? "bg-[var(--color-accent)] text-white border-[var(--color-accent)]"
                              : "border-[var(--border)] hover:border-[var(--color-accent)]"
                          }`}
                        >
                          {cat.label} ({cat.count})
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Rate Limit */}
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Rate Limit: {formData.rateLimit} req/min
                    </label>
                    <input
                      type="range"
                      min="1"
                      max="30"
                      value={formData.rateLimit}
                      onChange={(e) =>
                        setFormData((prev) => ({
                          ...prev,
                          rateLimit: parseInt(e.target.value),
                        }))
                      }
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-[var(--muted-foreground)]">
                      <span>Slower (safer)</span>
                      <span>Faster</span>
                    </div>
                  </div>

                  {/* Error Display */}
                  {error && (
                    <div className="p-3 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-800 rounded-lg text-red-800 dark:text-red-200 text-sm">
                      {error}
                    </div>
                  )}

                  <Button
                    type="submit"
                    size="lg"
                    loading={isScanning}
                    disabled={
                      (isCustomEndpoint && !formData.endpoint) ||
                      (!isCustomEndpoint && !formData.apiKey) ||
                      formData.categories.length === 0
                    }
                    className="w-full"
                  >
                    {isScanning ? "Scanning..." : "Start Security Scan"}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Info Panel */}
          <div className="space-y-4">
            <Card>
              <CardContent className="pt-4">
                <h3 className="font-semibold mb-2">
                  {isCustomEndpoint ? "Testing Your Chatbot" : "Direct API Test"}
                </h3>
                <p className="text-sm text-[var(--muted-foreground)] mb-3">
                  {isCustomEndpoint
                    ? "We'll send attack prompts to your endpoint and analyze the responses for vulnerabilities."
                    : "Test raw API security. Note: Results will be same for everyone using the same model."}
                </p>
                {isCustomEndpoint && (
                  <div className="text-xs text-[var(--muted-foreground)] space-y-1">
                    <p><strong>Simple JSON:</strong> We send {"{"}&quot;message&quot;: &quot;...&quot;{"}"}</p>
                    <p><strong>OpenAI Format:</strong> We send {"{"}&quot;messages&quot;: [...]{"}"}</p>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-4">
                <h3 className="font-semibold mb-2">23 Security Tests</h3>
                <ul className="text-sm text-[var(--muted-foreground)] space-y-2">
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 bg-red-500 rounded-full mt-1.5" />
                    10 prompt injection attacks
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 bg-yellow-500 rounded-full mt-1.5" />
                    8 jailbreak techniques
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-1.5" />
                    5 data extraction probes
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Results */}
        {scanResult && (
          <Card className="mt-8">
            <CardHeader>
              <CardTitle>Scan Results</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-4 gap-4 mb-6">
                <div className="text-center p-4 bg-[var(--muted)] rounded-lg">
                  <div className="text-3xl font-bold">{scanResult.result?.score ?? 0}</div>
                  <div className="text-sm text-[var(--muted-foreground)]">Security Score</div>
                </div>
                <div className="text-center p-4 bg-[var(--muted)] rounded-lg">
                  <div className="text-3xl font-bold">{scanResult.result?.total_tests ?? 0}</div>
                  <div className="text-sm text-[var(--muted-foreground)]">Tests Run</div>
                </div>
                <div className="text-center p-4 bg-green-100 dark:bg-green-900/30 rounded-lg">
                  <div className="text-3xl font-bold text-green-600">{scanResult.result?.passed ?? 0}</div>
                  <div className="text-sm text-[var(--muted-foreground)]">Passed</div>
                </div>
                <div className="text-center p-4 bg-red-100 dark:bg-red-900/30 rounded-lg">
                  <div className="text-3xl font-bold text-red-600">{scanResult.result?.failed ?? 0}</div>
                  <div className="text-sm text-[var(--muted-foreground)]">Vulnerabilities</div>
                </div>
              </div>

              {scanResult.result?.findings?.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-4">Findings</h4>
                  <div className="space-y-4">
                    {scanResult.result.findings.map((finding: any) => (
                      <div
                        key={finding.id}
                        className="p-4 border border-[var(--border)] rounded-lg"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium">{finding.attack_name}</span>
                          <span
                            className={`px-2 py-0.5 rounded text-xs font-medium ${
                              finding.severity === "critical"
                                ? "bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300"
                                : finding.severity === "high"
                                ? "bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-300"
                                : finding.severity === "medium"
                                ? "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300"
                                : "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
                            }`}
                          >
                            {finding.severity.toUpperCase()}
                          </span>
                        </div>
                        <p className="text-sm text-[var(--muted-foreground)] mb-2">
                          {finding.title}
                        </p>
                        <p className="text-sm">
                          <strong>Remediation:</strong> {finding.remediation}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {scanResult.result?.findings?.length === 0 && (
                <div className="text-center py-8 text-green-600">
                  <div className="text-4xl mb-2">🎉</div>
                  <div className="font-semibold">No vulnerabilities found!</div>
                  <div className="text-sm text-[var(--muted-foreground)]">
                    Your application passed all security tests.
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
}
