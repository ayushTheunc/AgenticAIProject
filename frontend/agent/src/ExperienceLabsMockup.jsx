import React, { useState } from "react";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Separator } from "./components/ui/separator";
import { ChevronLeft, Upload, LogIn } from "lucide-react";
import { gradeSubmission } from "./api";

const DEFAULT_RUBRIC = `{
  "correctness": {
    "weight": 0.5,
    "description": "Does the code run and meet the assignment specification?"
  },
  "style": {
    "weight": 0.2,
    "description": "Code clarity, naming, formatting, and structure."
  },
  "documentation": {
    "weight": 0.3,
    "description": "Comments, README, and overall explanation."
  }
}`;



function TopNav() {
  return (
    <div className="w-full bg-[#0f0f10] border-b border-neutral-800 sticky top-0 z-40">
      <div className="mx-auto max-w-7xl px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-lg bg-white text-black font-black w-8 h-8 grid place-items-center">XL</div>
          <div className="text-neutral-200">
            <div className="text-sm font-semibold leading-tight">CS Experience Labs @ UNC</div>
            <div className="text-xs text-neutral-400 flex items-center gap-2 mt-1">
              <Button variant="ghost" size="sm" className="px-2 h-6 text-neutral-300 hover:text-white">
                <ChevronLeft className="w-4 h-4 mr-1" /> Back
              </Button>
              <span className="text-neutral-600">/</span>
              <span className="truncate">COMP 110: Hello World!</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Input
            placeholder="Search"
            className="hidden md:block w-56 bg-neutral-900 border-neutral-800 text-neutral-100 placeholder:text-neutral-500"
          />
          <Button variant="outline" className="bg-neutral-900 border-neutral-700 text-neutral-200 hover:bg-neutral-800 hover:text-white">
            <LogIn className="w-4 h-4 mr-2" /> Sign In
          </Button>
        </div>
      </div>
    </div>
  );
}

function Sidebar({
  githubLink,
  setGithubLink,
  rubric,
  setRubric,
  testResults,
  setTestResults,
  onRunAgent,
  loading,
  error,
}) {
  return (
    <aside className="space-y-4">
      <Card className="bg-neutral-950/60 border-neutral-800">
        <CardHeader>
          <CardTitle className="text-neutral-200">Upload / Configure</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* GitHub repo link */}
          <div className="space-y-1">
            <div className="text-xs font-medium text-neutral-400 uppercase tracking-wide">
              GitHub Repository
            </div>
            <Input
              placeholder="https://github.com/student/repo"
              className="bg-neutral-900 border-neutral-800 text-neutral-100 placeholder:text-neutral-500"
              value={githubLink}
              onChange={(e) => setGithubLink(e.target.value)}
            />
            <p className="text-[11px] text-neutral-500">
              Paste the student&apos;s repo URL here. The agent will pull code directly
              from GitHub instead of a local upload.
            </p>
          </div>

          {/* Rubric JSON */}
          <div className="space-y-1">
            <div className="text-xs font-medium text-neutral-400 uppercase tracking-wide">
              Rubric (JSON)
            </div>
            <textarea
              rows={5}
              className="w-full rounded-md bg-neutral-900 border border-neutral-800 text-xs text-neutral-100 font-mono p-2 focus:outline-none focus:ring-2 focus:ring-indigo-500/70"
              value={rubric}
              onChange={(e) => setRubric(e.target.value)}
            />
            <p className="text-[11px] text-neutral-500">
              Edit criteria and weights as needed. This is sent to the AI grader as a
              structured rubric.
            </p>
          </div>

          {/* Optional test output */}
          <div className="space-y-1">
            <div className="text-xs font-medium text-neutral-400 uppercase tracking-wide">
              Test Results (optional)
            </div>
            <textarea
              rows={3}
              placeholder={"All unit tests passed.\n\nOr paste local test output here."}
              className="w-full rounded-md bg-neutral-900 border border-neutral-800 text-xs text-neutral-100 font-mono p-2 focus:outline-none focus:ring-2 focus:ring-indigo-500/70"
              value={testResults}
              onChange={(e) => setTestResults(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <Button
              className="w-full justify-center bg-indigo-600 hover:bg-indigo-500 text-white"
              onClick={onRunAgent}
              disabled={loading}
            >
              {loading ? "Running AI Grader…" : "Run AI Grader"}
            </Button>
            {error && (
              <p className="text-[11px] text-red-400">
                {error}
              </p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* You can keep your existing "Local Testing" / "Coming soon" cards here if you want.
          For now I’m leaving the rest of the sidebar unchanged. */}
    </aside>
  );
}


function SubmissionReview({ loading, gradeResult }) {
  const hasResult = !!gradeResult;

  // Normalize whatever the backend returns into readable text
  let analysisText = "";
  if (hasResult) {
    const a = gradeResult.analysis;
    if (Array.isArray(a)) {
      analysisText = a
        .map((item) =>
          typeof item === "string" ? item : JSON.stringify(item, null, 2)
        )
        .join("\n\n");
    } else if (typeof a === "string") {
      analysisText = a;
    } else if (a) {
      analysisText = JSON.stringify(a, null, 2);
    }
  }

  return (
    <section className="space-y-4">
      {/* Summary card */}
      <Card className="bg-neutral-950/60 border-neutral-800">
        <CardHeader>
          <CardTitle className="text-neutral-200">Submission Review</CardTitle>
        </CardHeader>
        <CardContent>
          {hasResult ? (
            <div className="space-y-2 text-sm text-neutral-200">
              <div>
                <span className="font-semibold">Status:</span>{" "}
                <span
                  className={
                    gradeResult.success ? "text-emerald-400" : "text-red-400"
                  }
                >
                  {gradeResult.success ? "Grading succeeded" : "Grading failed"}
                </span>
              </div>
              {gradeResult.error && (
                <div className="text-red-400 text-xs">
                  Error: {gradeResult.error}
                </div>
              )}
              <p className="text-xs text-neutral-400">
                Detailed criterion-level analysis is shown in the panel below.
              </p>
            </div>
          ) : (
            <ul className="text-neutral-300 space-y-2 text-sm list-disc list-inside">
              <li>Paste a GitHub repo and rubric on the left.</li>
              <li>Click &quot;Run AI Grader&quot; to fetch a structured review.</li>
              <li>
                The AI analysis will populate here and in the code panel below.
              </li>
            </ul>
          )}
        </CardContent>
      </Card>

      {/* Analysis / "code" panel */}
      <Card className="bg-neutral-950/60 border-neutral-800 overflow-hidden">
        <CardHeader className="py-3">
          <div className="text-xs uppercase tracking-widest text-neutral-400">
            {hasResult ? "AI rubric-aligned analysis" : "sample output"}
          </div>
        </CardHeader>
        <Separator className="bg-neutral-900" />
        <CardContent className="p-0">
          <pre className="text-sm leading-relaxed overflow-x-auto p-4 bg-[#0c0c0d] text-neutral-200 whitespace-pre-wrap">
            {hasResult
              ? analysisText || "No analysis text returned from backend."
              : `# Hello World with a for loop

# Once you run the AI grader, this panel will show
# rubric-aligned feedback for the student's submission.

for i in range(3):
    print("Hello, world!")`}
          </pre>
        </CardContent>
      </Card>
    </section>
  );
}


function InstructorComments() {
  return (
    <Card className="bg-neutral-950/60 border-neutral-800 h-full">
      <CardHeader>
        <CardTitle className="text-neutral-200">Instructor Comments</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="rounded-lg bg-neutral-900 border border-neutral-800 text-neutral-400 p-6 min-h-[560px]">
          No comments yet.
        </div>
      </CardContent>
    </Card>
  );
}

export default function ExperienceLabsMockup() {
  const [githubLink, setGithubLink] = useState("");
  const [rubric, setRubric] = useState(DEFAULT_RUBRIC);
  const [testResults, setTestResults] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [gradeResult, setGradeResult] = useState(null);

  async function handleRunAgent() {
    setError(null);

    if (!githubLink.trim()) {
      setError("Please enter a GitHub repo link.");
      return;
    }

    let rubricObject;
    try {
      rubricObject = JSON.parse(rubric);
    } catch {
      setError("Rubric must be valid JSON.");
      return;
    }

    setLoading(true);
    try {
      const res = await gradeSubmission({
        github_link: githubLink.trim(),
        rubric: rubricObject,
        test_results: testResults.trim() || undefined,
      });
      setGradeResult(res);
      if (!res.success && res.error) {
        setError(res.error);
      }
    } catch (e) {
      setError(e.message || "Something went wrong while calling the API.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <TopNav />
      <main className="mx-auto max-w-7xl px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-3">
            <Sidebar
              githubLink={githubLink}
              setGithubLink={setGithubLink}
              rubric={rubric}
              setRubric={setRubric}
              testResults={testResults}
              setTestResults={setTestResults}
              onRunAgent={handleRunAgent}
              loading={loading}
              error={error}
            />
          </div>
          <div className="lg:col-span-6">
            <SubmissionReview loading={loading} gradeResult={gradeResult} />
          </div>
          <div className="lg:col-span-3">
            <InstructorComments />
          </div>
        </div>
      </main>
    </div>
  );
}

