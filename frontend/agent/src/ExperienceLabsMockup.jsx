import React from "react";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Separator } from "./components/ui/separator";
import { ChevronLeft, Upload, LogIn } from "lucide-react";

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

function Sidebar() {
  return (
    <aside className="space-y-4">
      <Card className="bg-neutral-950/60 border-neutral-800">
        <CardHeader>
          <CardTitle className="text-neutral-200">Upload</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <Button className="w-full justify-start bg-neutral-900 hover:bg-neutral-800 border border-neutral-700 text-neutral-200" variant="outline">
            <Upload className="w-4 h-4 mr-2" /> Local Repo OR Github Repo
          </Button>
          <Button className="w-full justify-start bg-neutral-900 hover:bg-neutral-800 border border-neutral-700 text-neutral-200" variant="outline">
            Rubric
          </Button>
        </CardContent>
      </Card>

      <Card className="bg-neutral-950/60 border-neutral-800">
        <CardHeader>
          <CardTitle className="text-neutral-200">Local Testing</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-lg bg-neutral-900 border border-neutral-800 text-neutral-400 p-6 min-h-[120px]">
            Coming soon…
          </div>
        </CardContent>
      </Card>
    </aside>
  );
}

function SubmissionReview() {
  return (
    <section className="space-y-4">
      <Card className="bg-neutral-950/60 border-neutral-800">
        <CardHeader>
          <CardTitle className="text-neutral-200">Submission Review</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="text-neutral-300 space-y-2 text-sm list-decimal list-inside">
            <li>Criterion 1: <span className="text-green-400">10/10</span></li>
            <li>Criterion 2: <span className="text-yellow-400">7/10</span></li>
            <li>Criterion 4: <span className="text-red-400">0/10</span></li>
            <li>Criterion 5: <span className="text-green-400">10/10</span></li>
          </ul>
        </CardContent>
      </Card>

      <Card className="bg-neutral-950/60 border-neutral-800 overflow-hidden">
        <CardHeader className="py-3">
          <div className="text-xs uppercase tracking-widest text-neutral-400">python</div>
        </CardHeader>
        <Separator className="bg-neutral-900" />
        <CardContent className="p-0">
          <pre className="text-sm leading-relaxed overflow-x-auto p-4 bg-[#0c0c0d] text-neutral-200">
{`# Hello World with a for loop

for i in range(5):
    print(f"Hello, World! This is message number {i + 1}")
`}
          </pre>
        </CardContent>
      </Card>

      <Card className="bg-neutral-950/60 border-neutral-800">
        <CardHeader>
          <CardTitle className="text-neutral-200">Explanation :</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-lg bg-neutral-900 border border-neutral-800 text-neutral-400 p-6 min-h-[220px]">
            Write your explanation here…
          </div>
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
  return (
    <div>
      <TopNav />
      <main className="mx-auto max-w-7xl px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-3"><Sidebar /></div>
          <div className="lg:col-span-6"><SubmissionReview /></div>
          <div className="lg:col-span-3"><InstructorComments /></div>
        </div>
      </main>
    </div>
  );
}
