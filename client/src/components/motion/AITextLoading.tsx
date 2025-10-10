"use client";

/**
 * @author: @kokonutui
 * @description: AI Text Loading
 * @version: 1.0.0
 * @date: 2025-06-26
 * @license: MIT
 * @website: https://kokonutui.com
 * @github: https://github.com/kokonut-labs/kokonutui
 */

import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import { useEffect, useState } from "react";

interface AITextLoadingProps {
  texts?: string[];
  className?: string;
  interval?: number;
  compact?: boolean;
  staticText?: string;
}

export default function AITextLoading({
  texts = [
    "Thinking...",
    "Processing...",
    "Analyzing...",
    "Computing...",
    "Almost...",
  ],
  className,
  interval = 1500,
  compact = false,
  staticText,
}: AITextLoadingProps) {
  const [currentTextIndex, setCurrentTextIndex] = useState(0);

  useEffect(() => {
    if (staticText) {
      return; // no cycling when static text is provided
    }
    const timer = setInterval(() => {
      setCurrentTextIndex((prevIndex) => (prevIndex + 1) % texts.length);
    }, interval);

    return () => clearInterval(timer);
  }, [interval, texts.length, staticText]);

  return (
    <div className={`flex items-center ${compact ? "justify-start p-0" : "justify-center p-8"}`}>
      <motion.div
        className={compact ? "relative px-0 py-0 w-auto" : "relative px-4 py-2 w-full"}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4 }}
      >
        <AnimatePresence mode="wait">
          <motion.div
            key={staticText ? `static-${staticText}` : currentTextIndex}
            initial={{ opacity: 0, y: 20 }}
            animate={{
              opacity: 1,
              y: 0,
              backgroundPosition: ["200% center", "-200% center"],
            }}
            exit={{ opacity: 0, y: -20 }}
            transition={{
              opacity: { duration: 0.3 },
              y: { duration: 0.3 },
              backgroundPosition: {
                duration: 2.5,
                ease: "linear",
                repeat: Infinity,
              },
            }}
            className={cn(
              `flex ${compact ? "justify-start" : "justify-center"} ${compact ? "text-sm" : "text-3xl"} font-bold bg-gradient-to-r from-neutral-950 via-neutral-400 to-neutral-950 dark:from-white dark:via-neutral-600 dark:to-white bg-[length:200%_100%] bg-clip-text text-transparent whitespace-nowrap min-w-max`,
              className
            )}
          >
            {staticText ?? texts[currentTextIndex]}
          </motion.div>
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
