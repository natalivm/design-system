/** Cashout iOS components. Web previews of SwiftUI views; props mirror the Swift initializers. */
import type { ReactNode } from "react";

export interface ButtonProps {
  /** filled = the one primary action; plain = text-only secondary action. */
  variant?: "filled" | "plain";
  fullWidth?: boolean;
  disabled?: boolean;
  /** Shows a spinner and disables the button. */
  loading?: boolean;
  loadingLabel?: string;
  onClick?: () => void;
  children?: ReactNode;
}

export interface AmountHeroProps {
  state?: "earned" | "empty" | "pending" | "success";
  /** Raw number; formatting is done with the currency and locale. */
  amount: number;
  /** ISO 4217 code, e.g. "USD", "EUR". */
  currency?: string;
  locale?: string;
  eyebrow?: string;
  subtitle?: string;
  /** Slot under the subtitle, e.g. the History Pill. */
  children?: ReactNode;
}

export interface PillProps {
  /** Translucent white fill for use on the green hero. */
  glass?: boolean;
  icon?: string;
  onClick?: () => void;
  children?: ReactNode;
}

export interface InfoRowProps {
  /** Seconds until stars convert; shown as "3h 45m". */
  secondsLeft?: number;
  children?: ReactNode;
}

export interface CountdownProps {
  seconds?: number;
  /** Tick every second. */
  live?: boolean;
  size?: "large" | "small" | "card";
  /** Caption above the time on the card size. */
  label?: string;
}

export interface HistoryItem {
  date: string;
  amount: number;
  currency?: string;
  status?: "success" | "pending" | "failed";
}
export interface HistoryListProps {
  items: HistoryItem[];
  currency?: string;
  locale?: string;
}

export interface StatTileProps {
  label: string;
  value: string;
  /** "star" for the reward star, or an image URL. */
  icon?: string;
}

export interface InlineMessageProps {
  tone?: "danger" | "info";
  children: ReactNode;
}

export interface TabBarProps {
  tabs?: { id: "home" | "cashout" | "history" | "profile"; label: string }[];
  selected?: string;
}

export interface CashoutSheetProps {
  state?: "earned" | "pending" | "empty" | "success";
  amount?: number;
  currency?: string;
  locale?: string;
  /** Seconds left on the pending countdown. */
  seconds?: number;
  /** Seconds until conversion, for InfoRow. */
  secondsLeft?: number;
  live?: boolean;
  loading?: boolean;
  limitReached?: boolean;
}

export declare function Button(props: ButtonProps): JSX.Element;
export declare function AmountHero(props: AmountHeroProps): JSX.Element;
export declare function Pill(props: PillProps): JSX.Element;
export declare function InfoRow(props: InfoRowProps): JSX.Element;
export declare function Countdown(props: CountdownProps): JSX.Element;
export declare function HistoryList(props: HistoryListProps): JSX.Element;
export declare function StatTile(props: StatTileProps): JSX.Element;
export declare function InlineMessage(props: InlineMessageProps): JSX.Element;
export declare function TabBar(props: TabBarProps): JSX.Element;
export declare function CashoutSheet(props: CashoutSheetProps): JSX.Element;
