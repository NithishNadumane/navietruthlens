import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Loader2, Sparkles, FileText, Trash2 } from "lucide-react";

interface NewsInputProps {
  onAnalyze: (text: string) => void;
  isProcessing: boolean;
}

const SAMPLE_REAL = `The Federal Reserve on Wednesday raised its benchmark interest rate by a quarter percentage point, continuing its campaign to cool inflation that remains well above its 2% target. The central bank also signaled that it expects to keep raising rates in coming months. The decision was widely expected by financial markets and came as recent economic data showed that inflation, while declining, is still elevated. Fed Chair Jerome Powell said the economy continues to show resilience, though he acknowledged recent banking turmoil could tighten credit conditions.`;

const SAMPLE_FAKE = `BREAKING: Scientists at CERN have accidentally opened a portal to another dimension during a routine particle experiment! The portal, which appeared as a glowing purple vortex in the main laboratory, remained open for approximately 47 seconds before researchers managed to shut it down. Three scientists who were standing near the portal claim they saw "strange creatures" on the other side. The government is desperately trying to cover this up but we have EXCLUSIVE footage!! Share before this gets deleted!!!`;

export const NewsInput = ({ onAnalyze, isProcessing }: NewsInputProps) => {
  const [text, setText] = useState("");

  const handleAnalyze = () => {
    if (text.trim().length >= 20) {
      onAnalyze(text.trim());
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-card/80 backdrop-blur-sm rounded-3xl shadow-hard border-2 border-primary/20 p-8 md:p-10 space-y-6 hover:border-primary/30 transition-all duration-300">
        <div className="space-y-3">
          <h2 className="text-2xl md:text-3xl font-display font-bold flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-gradient-to-br from-primary to-primary-light shadow-glow-primary">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <span className="bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
              Analyze News Article
            </span>
          </h2>
          <p className="text-muted-foreground text-base md:text-lg">
            Paste or type a news article below to check if it's real or fake
          </p>
        </div>

        <div className="space-y-3">
          <textarea
            id="news-text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your news article text here..."
            disabled={isProcessing}
            rows={8}
            className="w-full resize-none rounded-xl border-2 border-border bg-background/80 backdrop-blur-sm p-4 text-base focus:border-primary/50 focus:shadow-glow-primary focus:outline-none focus:ring-0 transition-all duration-300 placeholder:text-muted-foreground/50"
          />
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>{text.length} characters • {text.trim().split(/\s+/).filter(Boolean).length} words</span>
            {text.length > 0 && text.length < 20 && (
              <span className="text-destructive">Minimum 20 characters required</span>
            )}
          </div>
        </div>

        {/* Sample Text Buttons */}
        <div className="flex flex-wrap gap-3">
          <span className="text-sm text-muted-foreground self-center font-medium">Try samples:</span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setText(SAMPLE_REAL)}
            disabled={isProcessing}
            className="border-2 border-emerald-500/30 text-emerald-600 hover:bg-emerald-500/10 hover:border-emerald-500 rounded-lg font-semibold"
          >
            📰 Real News
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setText(SAMPLE_FAKE)}
            disabled={isProcessing}
            className="border-2 border-red-500/30 text-red-500 hover:bg-red-500/10 hover:border-red-500 rounded-lg font-semibold"
          >
            🚨 Fake News
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

        <Button
          id="analyze-button"
          onClick={handleAnalyze}
          disabled={isProcessing || text.trim().length < 20}
          className="w-full h-14 text-lg font-bold bg-gradient-to-r from-primary via-secondary to-secondary-light hover:from-primary-light hover:via-secondary-light hover:to-secondary-glow transition-all shadow-glow-primary hover:shadow-glow-secondary hover:scale-[1.02] rounded-xl"
        >
          {isProcessing ? (
            <>
              <Loader2 className="w-6 h-6 mr-2 animate-spin" />
              Analyzing with Navie Model...
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
