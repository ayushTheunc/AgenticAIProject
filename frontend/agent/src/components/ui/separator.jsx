import * as React from "react";
import { cn } from "lib/utils";

export function Separator({ className, ...props }) {
  return (
    <div
      className={cn("shrink-0 bg-border", className)}
      style={{ height: "1px", width: "100%" }}
      {...props}
    />
  );
}
