import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Loader2, Sparkles, FileText, Newspaper, Trash2, Languages } from "lucide-react";
import type { InputMode } from "@/lib/api";

interface NewsInputProps {
  onAnalyze: (text: string, mode: InputMode) => void;
  isProcessing: boolean;
}

const SAMPLE_HEADLINE_REAL = `RBI keeps repo rate unchanged at 6.5% for seventh consecutive time`;
const SAMPLE_HEADLINE_FAKE = `BREAKING: Scientists discover cure for all cancers, government hiding it!`;

const SAMPLE_ARTICLE_REAL = `The Federal Reserve on Wednesday raised its benchmark interest rate by a quarter percentage point, continuing its campaign to cool inflation that remains well above its 2% target. The central bank also signaled that it expects to keep raising rates in coming months. The decision was widely expected by financial markets and came as recent economic data showed that inflation, while declining, is still elevated. Fed Chair Jerome Powell said the economy continues to show resilience, though he acknowledged recent banking turmoil could tighten credit conditions.`;
const SAMPLE_ARTICLE_FAKE = `BREAKING: Scientists at CERN have accidentally opened a portal to another dimension during a routine particle experiment! The portal, which appeared as a glowing purple vortex in the main laboratory, remained open for approximately 47 seconds before researchers managed to shut it down. Three scientists who were standing near the portal claim they saw "strange creatures" on the other side. The government is desperately trying to cover this up but we have EXCLUSIVE footage!! Share before this gets deleted!!!`;

export const NewsInput = ({ onAnalyze, isProcessing }: NewsInputProps) => {
  const [text, setText] = useState("");
  const [mode, setMode] = useState<InputMode>("article");

  const isHeadline = mode === "headline";

  // Minimum: 3 words for headline, 20 chars for article
  const isValid = isHeadline
    ? text.trim().split(/\s+/).filter(Boolean).length >= 3
    : text.trim().length >= 20;

  const handleAnalyze = () => {
    if (isValid) onAnalyze(text.trim(), mode);
  };

  const handleModeChange = (newMode: InputMode) => {
    setMode(newMode);
    setText("");
  };

  const sampleReal    = isHeadline ? SAMPLE_HEADLINE_REAL    : SAMPLE_ARTICLE_REAL;
  const sampleFake    = isHeadline ? SAMPLE_HEADLINE_FAKE    : SAMPLE_ARTICLE_FAKE;
  const placeholder   = isHeadline
    ? "Paste or type a news headline here... (supports ಕನ್ನಡ Kannada)"
    : "Paste or type a full news article here... (supports ಕನ್ನಡ Kannada)";
  const minHint       = isHeadline ? "Minimum 3 words required" : "Minimum 20 characters required";
  const showMinHint   = isHeadline
    ? text.trim().split(/\s+/).filter(Boolean).length < 3 && text.length > 0
    : text.length > 0 && text.length < 20;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-card/80 backdrop-blur-sm rounded-3xl shadow-hard border-2 border-primary/20 p-8 md:p-10 space-y-6 hover:border-primary/30 transition-all duration-300">

        {/* Header */}
        <div className="space-y-3">
          <h2 className="text-2xl md:text-3xl font-display font-bold flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-gradient-to-br from-primary to-primary-light shadow-glow-primary">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <span className="bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
              Analyze News
            </span>
          </h2>
          <p className="text-muted-foreground text-base md:text-lg">
            Detect misinformation using just a <strong>headline</strong> or a full <strong>article</strong>
          </p>
        </div>

        {/* Mode Toggle */}
        <div className="flex gap-2 p-1.5 bg-muted/60 rounded-xl border border-border w-fit">
          <button
            id="mode-headline"
            onClick={() => handleModeChange("headline")}
            disabled={isProcessing}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 ${
              isHeadline
                ? "bg-gradient-to-r from-primary to-secondary text-white shadow-glow-primary scale-[1.02]"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Newspaper className="w-4 h-4" />
            Headline
          </button>
          <button
            id="mode-article"
            onClick={() => handleModeChange("article")}
            disabled={isProcessing}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 ${
              !isHeadline
                ? "bg-gradient-to-r from-primary to-secondary text-white shadow-glow-primary scale-[1.02]"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <FileText className="w-4 h-4" />
            Full Article
          </button>
        </div>

        {/* Kannada hint — always shown */}
        <div className="flex items-center gap-2 text-sm text-amber-600 dark:text-amber-400 bg-amber-500/10 border border-amber-500/20 rounded-lg px-3 py-2">
          <Languages className="w-4 h-4 shrink-0" />
          <span>
            Supports <strong>Kannada (ಕನ್ನಡ)</strong> — your {isHeadline ? 'headline' : 'article'} will be auto-translated to English before analysis.
          </span>
        </div>

        {/* Textarea */}
        <div className="space-y-3">
          <textarea
            id="news-text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={placeholder}
            disabled={isProcessing}
            rows={isHeadline ? 3 : 8}
            className="w-full resize-none rounded-xl border-2 border-border bg-background/80 backdrop-blur-sm p-4 text-base focus:border-primary/50 focus:shadow-glow-primary focus:outline-none focus:ring-0 transition-all duration-300 placeholder:text-muted-foreground/50"
          />
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>
              {text.length} characters • {text.trim().split(/\s+/).filter(Boolean).length} words
            </span>
            {showMinHint && (
              <span className="text-destructive">{minHint}</span>
            )}
          </div>
        </div>

        {/* Sample Buttons */}
        <div className="flex flex-wrap gap-3">
          <span className="text-sm text-muted-foreground self-center font-medium">Try samples:</span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setText(sampleReal)}
            disabled={isProcessing}
            className="border-2 border-emerald-500/30 text-emerald-600 hover:bg-emerald-500/10 hover:border-emerald-500 rounded-lg font-semibold"
          >
            📰 Real {isHeadline ? "Headline" : "Article"}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setText(sampleFake)}
            disabled={isProcessing}
            className="border-2 border-red-500/30 text-red-500 hover:bg-red-500/10 hover:border-red-500 rounded-lg font-semibold"
          >
            🚨 Fake {isHeadline ? "Headline" : "Article"}
          </Button>
          {text.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setText("")}
              disabled={isProcessing}
              className="text-muted-foreground hover:text-destructive rounded-lg"
            >
              <Trash2 className="w-4 h-4 mr-1" />
              Clear
            </Button>
          )}
        </div>

        {/* Analyze Button */}
        <Button
          id="analyze-button"
          onClick={handleAnalyze}
          disabled={isProcessing || !isValid}
          className="w-full h-14 text-lg font-bold bg-gradient-to-r from-primary via-secondary to-secondary-light hover:from-primary-light hover:via-secondary-light hover:to-secondary-glow transition-all shadow-glow-primary hover:shadow-glow-secondary hover:scale-[1.02] rounded-xl"
        >
          {isProcessing ? (
            <>
              <Loader2 className="w-6 h-6 mr-2 animate-spin" />
              Analyzing {isHeadline ? "Headline" : "Article"}...
            </>
          ) : (
            <>
              <Sparkles className="w-6 h-6 mr-2" />
              Detect Fake News
            </>
          )}
        </Button>
      </div>
    </div>
  );
};
