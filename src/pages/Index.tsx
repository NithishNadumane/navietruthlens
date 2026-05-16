import { useState } from "react";
import { NewsInput } from "@/components/truthlens/NewsInput";
import { PredictionResultCard } from "@/components/truthlens/PredictionResult";
import { ModelMetrics } from "@/components/truthlens/ModelMetrics";
import { HowItWorks } from "@/components/truthlens/HowItWorks";
import { HistoryPanel, addToHistory } from "@/components/truthlens/HistoryPanel";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ShieldCheck, BarChart3, Cpu, History, Sparkles } from "lucide-react";
import { predictNews } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";
import type { PredictionResult } from "@/lib/api";

const Index = () => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [activeTab, setActiveTab] = useState("detect");
  const { toast } = useToast();

  const handleAnalyze = async (text: string) => {
    setIsProcessing(true);
    setResult(null);

    try {
      const prediction = await predictNews(text);
      setResult(prediction);
      addToHistory(text, prediction.prediction, prediction.confidence);
      setActiveTab("detect");

      toast({
        title: prediction.prediction === "REAL" ? "✅ News Verified" : "🚨 Fake News Detected",
        description: `Confidence: ${prediction.confidence}%`,
      });
    } catch (error: any) {
      console.error("Prediction error:", error);
      toast({
        title: "Analysis Failed",
        description: error.message || "Could not connect to the backend. Make sure the Flask server is running.",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Animated Background Mesh */}
      <div className="fixed inset-0 bg-gradient-mesh pointer-events-none opacity-50" />

      {/* Floating Orbs */}
      <div className="fixed top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl animate-float pointer-events-none" />
      <div className="fixed bottom-20 right-10 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-float pointer-events-none" style={{ animationDelay: '1s' }} />
      <div className="fixed top-1/2 left-1/2 w-80 h-80 bg-accent/20 rounded-full blur-3xl animate-float pointer-events-none" style={{ animationDelay: '2s' }} />

      <div className="container mx-auto px-4 py-8 md:py-12 relative z-10">
        {/* Hero Header */}
        <div className="text-center mb-12 md:mb-16 space-y-5 animate-fade-in-up">
          <div className="inline-flex items-center justify-center relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-primary via-secondary to-accent rounded-3xl blur-xl opacity-60 group-hover:opacity-100 transition-opacity animate-pulse-glow" />
            <div className="relative w-18 h-18 md:w-20 md:h-20 rounded-3xl bg-gradient-to-br from-primary via-secondary to-accent flex items-center justify-center shadow-glow-primary">
              <ShieldCheck className="w-9 h-9 md:w-10 md:h-10 text-white" />
            </div>
          </div>

          <div className="space-y-3">
            <h1 className="text-5xl md:text-7xl font-display font-black tracking-tighter">
              <span className="bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent animate-shimmer bg-[length:200%_100%]">
                TruthLens
              </span>
            </h1>
            <div className="flex items-center justify-center gap-2 text-primary">
              <Sparkles className="w-4 h-4 md:w-5 md:h-5 animate-pulse" />
              <span className="text-xs md:text-sm font-semibold uppercase tracking-wider">Deep Learning Fake News Detection</span>
              <Sparkles className="w-4 h-4 md:w-5 md:h-5 animate-pulse" />
            </div>
          </div>

          <p className="text-base md:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Detect misinformation instantly with <span className="text-primary font-semibold">Naive Bayes Classification</span> and <span className="text-secondary font-semibold">NLP preprocessing</span>. Powered by PyTorch.
          </p>
        </div>

        {/* Main Content Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full max-w-2xl mx-auto grid-cols-4 mb-10 h-12 md:h-14 bg-card/50 backdrop-blur-sm border-2 border-primary/20 p-1 shadow-medium">
            <TabsTrigger
              value="detect"
              className="flex items-center gap-1.5 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-primary data-[state=active]:to-primary-light data-[state=active]:text-white data-[state=active]:shadow-glow-primary transition-all duration-300 text-xs md:text-sm"
            >
              <ShieldCheck className="w-4 h-4" />
              <span className="font-semibold hidden sm:inline">Detect</span>
            </TabsTrigger>
            <TabsTrigger
              value="metrics"
              className="flex items-center gap-1.5 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-secondary data-[state=active]:to-secondary-light data-[state=active]:text-white data-[state=active]:shadow-glow-secondary transition-all duration-300 text-xs md:text-sm"
            >
              <BarChart3 className="w-4 h-4" />
              <span className="font-semibold hidden sm:inline">Metrics</span>
            </TabsTrigger>
            <TabsTrigger
              value="how"
              className="flex items-center gap-1.5 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-accent data-[state=active]:to-accent-light data-[state=active]:text-white data-[state=active]:shadow-glow-accent transition-all duration-300 text-xs md:text-sm"
            >
              <Cpu className="w-4 h-4" />
              <span className="font-semibold hidden sm:inline">How It Works</span>
            </TabsTrigger>
            <TabsTrigger
              value="history"
              className="flex items-center gap-1.5 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-emerald-600 data-[state=active]:to-teal-500 data-[state=active]:text-white transition-all duration-300 text-xs md:text-sm"
            >
              <History className="w-4 h-4" />
              <span className="font-semibold hidden sm:inline">History</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="detect" className="space-y-10">
            <div className="animate-scale-in">
              <NewsInput onAnalyze={handleAnalyze} isProcessing={isProcessing} />
            </div>

            {result && (
              <div className="animate-fade-in-up">
                <PredictionResultCard result={result} />
              </div>
            )}
          </TabsContent>

          <TabsContent value="metrics">
            <ModelMetrics />
          </TabsContent>

          <TabsContent value="how">
            <HowItWorks />
          </TabsContent>

          <TabsContent value="history">
            <HistoryPanel />
          </TabsContent>
        </Tabs>

        {/* Footer */}
        <footer className="mt-20 text-center text-sm text-muted-foreground/60 space-y-1 pb-8">
          <p className="font-semibold text-muted-foreground/80">TruthLens — Data Mining Project</p>
          <p>Built with PyTorch • NBC • NLTK • React • Flask</p>
        </footer>
      </div>
    </div>
  );
};

export default Index;
