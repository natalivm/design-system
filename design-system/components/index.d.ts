/** BestPlay design system components. Web previews of SwiftUI views; props mirror the Swift initializers.
 *  bundle.js and onboarding.js are plain scripts (not modules): load React 18 first, then they add
 *  every component to `window.Cashout`. */
import type { CSSProperties, ReactNode } from "react";

export interface ButtonProps {
  /** filled = the one primary action; plain = text-only secondary action. */
  variant?: "filled" | "plain";
  fullWidth?: boolean;
  disabled?: boolean;
  /** Shows a spinner and disables the button. */
  loading?: boolean;
  loadingLabel?: string;
  onClick?: () => void;
  className?: string;
  style?: CSSProperties;
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
  /** Text shown instead of the formatted amount. */
  display?: string;
  className?: string;
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
  onSelect?: (id: string) => void;
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

/* ---------- onboarding ---------- */
export interface MissionRowProps {
  title: ReactNode;
  coins: number;
  state?: "go" | "progress" | "claim" | "claimed";
  progress?: number;
  total?: number;
  onAction?: () => void;
}
export interface MissionCardProps {
  title?: string;
  timer?: string;
  /** Missions done, 0 to 3. */
  done?: number;
  finished?: boolean;
  collapsed?: boolean;
  children?: ReactNode;
}
export interface CoachMarkProps {
  /** The control the hint points at; it stays lit above the dim. */
  target: ReactNode;
  children: ReactNode;
}
export interface RewardCardProps {
  tone?: "welcome" | "congrats" | "boost";
  title?: string;
  subtitle?: string;
  amount?: string;
  cta?: string;
  /** Text link under the card; defaults per tone ("Claim 1,500", "Skip"). */
  dismiss?: string;
  onAction?: () => void;
  onDismiss?: () => void;
}
export interface PopupProps {
  size?: "compact" | "standard" | "hero";
  /** "dark" sets a dark card with white text (default background: the overlay token). */
  card?: "light" | "dark";
  /** Card background, e.g. a gradient. */
  bg?: string;
  /** Header background. */
  headBg?: string;
  head?: ReactNode;
  curve?: boolean;
  eyebrow?: string;
  /** Art that pokes out above the card. */
  over?: ReactNode;
  title?: string;
  text?: string;
  amount?: string;
  action?: string;
  tone?: "claim" | "boost" | "offer";
  /** Adds the Watch ad tag to the button. */
  ad?: boolean;
  dismiss?: string;
  onAction?: () => void;
  onDismiss?: () => void;
  className?: string;
  children?: ReactNode;
}

/* ---------- 2x coins ---------- */
export interface FlipTimerProps {
  /** Seconds left, or six digits "hhmmss". */
  value?: number | string;
  size?: "large" | "small";
}
export interface TimePillProps { children?: ReactNode; }
export interface BoostButtonProps {
  size?: "popup" | "banner";
  onAction?: () => void;
  children?: ReactNode;
}
export interface EventBannerProps {
  state?: "offer" | "active";
  value?: number | string;
  label?: string;
  endsIn?: string;
  /** Offer: Start now. */
  onAction?: () => void;
  /** Active: tapping the banner opens the progress pop-up. */
  onOpen?: () => void;
}
export interface BoostPopupProps {
  state?: "offer" | "active" | "progress" | "over";
  value?: number | string;
  left?: string;
  base?: string;
  total?: string;
  label?: string;
  dismiss?: string;
  onAction?: () => void;
  onDismiss?: () => void;
}

type C<P> = (props: P) => JSX.Element;
export interface CashoutComponents {
  Button: C<ButtonProps>;
  AmountHero: C<AmountHeroProps>;
  Pill: C<PillProps>;
  InfoRow: C<InfoRowProps>;
  Countdown: C<CountdownProps>;
  HistoryList: C<HistoryListProps>;
  StatTile: C<StatTileProps>;
  InlineMessage: C<InlineMessageProps>;
  TabBar: C<TabBarProps>;
  CashoutSheet: C<CashoutSheetProps>;
  MissionRow: C<MissionRowProps>;
  MissionCard: C<MissionCardProps>;
  CoachMark: C<CoachMarkProps>;
  RewardCard: C<RewardCardProps>;
  Popup: C<PopupProps> & { art: Record<string, string> };
  FlipTimer: C<FlipTimerProps>;
  TimePill: C<TimePillProps>;
  AdTag: C<{}>;
  BoostTag: C<{}>;
  BoostButton: C<BoostButtonProps>;
  EventBanner: C<EventBannerProps>;
  BoostPopup: C<BoostPopupProps>;
  /** Docs helpers. */
  Copy: C<{ label?: string; code: string }>;
  Demo: C<{ caption?: string; children?: ReactNode }>;
  format: { money(amount: number, currency?: string, locale?: string): string; clock(seconds: number): { text: string; spoken: string } };
  assets: Record<string, string>;
}

declare global {
  interface Window { Cashout: CashoutComponents; }
}
