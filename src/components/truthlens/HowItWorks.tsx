import { Card } from "@/components/ui/card";
import { FileText, Scissors, Binary, BrainCircuit, CheckCircle, ArrowRight } from "lucide-react";

const steps = [
  {
    icon: FileText,
    title: "Input Text",
    description: "Raw news article text is received for analysis",
    detail: "User pastes or types the news content",
    color: "from-blue-600 to-cyan-500",
  },
  {
    icon: Scissors,
    title: "NLP Preprocessing",
    description: "Tokenization, stop-word removal, text normalization",
    detail: "NLTK cleans and standardizes the text",
    color: "from-purple-600 to-pink-500",
  },
{
  icon: Binary,
  title: "TF-IDF Vectorization",
  description: "Text converted into numerical feature vectors using TF-IDF",
  detail: "Captures important words based on frequency and relevance",
  color: "from-orange-600 to-amber-500",
},
{
  icon: BrainCircuit,
  title: "Naive Bayes Classification",
  description: "Naive Bayes model analyzes text patterns for prediction",
  detail: "Multinomial Naive Bayes used for fake news classification",
  color: "from-emerald-600 to-teal-500",
},
  {
    icon: CheckCircle,
    title: "Prediction",
    description: "Binary classification: Real or Fake with confidence score",
    detail: "Sigmoid output → probability → verdict",
    color: "from-red-600 to-rose-500",
  },
];

export const HowItWorks = () => {
  return (
    <div className="space-y-8">
      {/* Section Header */}
      <div className="text-center space-y-2">
        <h2 className="text-3xl md:text-4xl font-display font-black">
          <span className="bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
            How TruthLens Works
          </span>
        </h2>
        <p className="text-muted-foreground text-base md:text-lg max-w-2xl mx-auto">
          Deep Learning pipeline combining NLP preprocessing with LSTM neural networks
        </p>
      </div>

      {/* Pipeline Steps */}
      <div className="max-w-4xl mx-auto">
        <div className="relative">
          {steps.map((step, index) => (
            <div key={index} className="relative">
              {/* Step Card */}
              <div
                className="flex items-start gap-4 md:gap-6 animate-fade-in-up"
                style={{ animationDelay: `${index * 0.15}s` }}
              >
                {/* Left: Icon + Connector */}
                <div className="flex flex-col items-center flex-shrink-0">
                  <div
                    className={`w-14 h-14 md:w-16 md:h-16 rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center shadow-medium animate-scale-in`}
                    style={{ animationDelay: `${index * 0.15}s` }}
                  >
                    <step.icon className="w-7 h-7 md:w-8 md:h-8 text-white" />
                  </div>
                  {index < steps.length - 1 && (
                    <div className="w-0.5 h-8 bg-gradient-to-b from-primary/40 to-transparent my-2" />
                  )}
                </div>

                {/* Right: Content */}
                <Card className="flex-1 p-4 md:p-5 border-2 border-primary/10 hover:border-primary/30 transition-all duration-300 hover:-translate-y-0.5 bg-card/80 backdrop-blur-sm mb-4">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs font-bold text-primary/70 uppercase tracking-wider">
                          Step {index + 1}
                        </span>
                      </div>
                      <h3 className="text-lg font-display font-bold text-foreground">
                        {step.title}
                      </h3>
                      <p className="text-muted-foreground text-sm mt-1">
                        {step.description}
                      </p>
                      <p className="text-xs text-primary/80 font-mono mt-2 bg-primary/5 px-2 py-1 rounded-md inline-block">
                        {step.detail}
                      </p>
                    </div>
                    {index < steps.length - 1 && (
                      <ArrowRight className="w-5 h-5 text-muted-foreground/40 flex-shrink-0 mt-2 hidden md:block" />
                    )}
                  </div>
                </Card>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Tech Stack */}
      <Card className="max-w-4xl mx-auto p-6 border-2 border-primary/10 bg-card/80 backdrop-blur-sm">
        <h3 className="text-lg font-display font-bold text-foreground mb-4">
          🛠️ Technology Stack
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { name: "PyTorch", desc: "LSTM Model" },
            { name: "NLTK", desc: "Text Preprocessing" },
            { name: "Scikit-learn", desc: "Evaluation Metrics" },
            { name: "Flask", desc: "API Backend" },
            { name: "React", desc: "Frontend UI" },
            { name: "Recharts", desc: "Visualizations" },
            { name: "Pandas", desc: "Data Processing" },
            { name: "NumPy", desc: "Numerical Ops" },
          ].map((tech, i) => (
            <div
              key={i}
              className="p-3 rounded-xl bg-gradient-to-br from-muted/80 to-muted/40 border border-border text-center hover:border-primary/30 transition-all duration-300"
            >
              <div className="font-bold text-sm text-foreground">{tech.name}</div>
              <div className="text-xs text-muted-foreground mt-0.5">{tech.desc}</div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
