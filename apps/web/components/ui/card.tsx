import type { HTMLAttributes, ReactNode } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

export function Card({ children, className = "", ...props }: CardProps) {
  return (
    <div
      className={`
        bg-[var(--background)]
        border border-[var(--border)]
        rounded-xl
        shadow-sm
        ${className}
      `}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  children,
  className = "",
  ...props
}: CardProps) {
  return (
    <div
      className={`px-6 py-4 border-b border-[var(--border)] ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardTitle({
  children,
  className = "",
  ...props
}: CardProps) {
  return (
    <h3
      className={`text-lg font-semibold text-[var(--foreground)] ${className}`}
      {...props}
    >
      {children}
    </h3>
  );
}

export function CardDescription({
  children,
  className = "",
  ...props
}: CardProps) {
  return (
    <p
      className={`text-sm text-[var(--muted-foreground)] mt-1 ${className}`}
      {...props}
    >
      {children}
    </p>
  );
}

export function CardContent({
  children,
  className = "",
  ...props
}: CardProps) {
  return (
    <div className={`px-6 py-4 ${className}`} {...props}>
      {children}
    </div>
  );
}

export function CardFooter({
  children,
  className = "",
  ...props
}: CardProps) {
  return (
    <div
      className={`px-6 py-4 border-t border-[var(--border)] ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
