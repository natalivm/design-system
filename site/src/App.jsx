import { useEffect, useRef, useState } from 'react';
import CoinHero from './components/CoinHero.jsx';
import { tokens, swiftName, RULES, TYPE, SNIPPETS, MOTION, LINKS } from './data.js';

const C = window.Cashout;
const BASE = import.meta.env.BASE_URL;

/* ---------- small helpers ---------- */
function useReveal() {
  useEffect(() => {
    const els = document.querySelectorAll('[data-reveal]');
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return undefined;
    els.forEach((el) => el.classList.add('pre'));
    const io = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -10% 0px' });
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);
}

function copy(text) {
  try { return navigator.clipboard.writeText(text).then(() => true, () => false); } catch (e) { return Promise.resolve(false); }
}

function CopyChip({ text, label }) {
  const [done, setDone] = useState(false);
  return (
    <button className="copychip" onClick={() => copy(text).then((ok) => { setDone(ok); setTimeout(() => setDone(false), 1300); })}>
      <code>{label || text}</code><span>{done ? 'Copied' : 'Copy'}</span>
    </button>
  );
}

function CodeBlock({ code }) {
  const [done, setDone] = useState(false);
  return (
    <div className="codeblock">
      <pre>{code}</pre>
      <button onClick={() => copy(code).then((ok) => { setDone(ok); setTimeout(() => setDone(false), 1300); })}>{done ? 'Copied' : 'Copy'}</button>
    </div>
  );
}

function Section({ id, eyebrow, title, lead, children, dark }) {
  return (
    <section id={id} className={'section' + (dark ? ' dark' : '')}>
      <div className="wrap">
        <header className="section-head" data-reveal>
          <span className="eyebrow">{eyebrow}</span>
          <h2>{title}</h2>
          {lead ? <p>{lead}</p> : null}
        </header>
        {children}
      </div>
    </section>
  );
}

/* ---------- sections ---------- */
function Hero() {
  const colors = tokens.color.tokens.length;
  const styles = tokens.type.groups.reduce((n, g) => n + g.styles.length, 0);
  return (
    <header className="hero">
      <CoinHero />
      <nav className="topnav wrap">
        <span className="brand">Cashout iOS</span>
        <div className="navlinks">
          <a href="#color">Color</a><a href="#type">Type</a><a href="#components">Components</a><a href="#motion">Motion</a><a href="#prototype">Prototype</a>
        </div>
      </nav>
      <div className="hero-copy wrap">
        <span className="eyebrow light">Design system · v1</span>
        <h1>Every cent,<br />designed for iOS.</h1>
        <p>Tokens, components, motion and a working prototype for the cash-out flow, rebuilt from Figma with Apple's conventions.</p>
        <div className="hero-ctas">
          <a className="cta primary" href="#prototype">Try the prototype</a>
          <a className="cta ghost" href="#color">Explore the tokens</a>
        </div>
        <ul className="stats">
          <li><b>{colors}</b>colors, light and dark</li>
          <li><b>{styles}</b>text styles</li>
          <li><b>10</b>components</li>
          <li><b>7</b>motion patterns</li>
        </ul>
      </div>
    </header>
  );
}

function Rules() {
  return (
    <Section id="rules" eyebrow="Principles" title="Eight rules, one page" lead="What changed from the Figma file, and what to do from now on.">
      <div className="rules">
        {RULES.map(([k, d, x], i) => (
          <article key={k} className="rule" data-reveal style={{ '--d': i * 40 + 'ms' }}>
            <span className="rule-k">{k}</span>
            <p className="rule-do">{d}</p>
            <p className="rule-not">Instead of {x}</p>
          </article>
        ))}
      </div>
    </Section>
  );
}

function Colors() {
  const [mode, setMode] = useState('light');
  const val = (t) => (typeof t.value === 'string' ? t.value : t.value[mode] || t.value.light);
  return (
    <Section id="color" eyebrow="Foundations" title="Color" lead="Tap a swatch to copy its Swift name. Every text pairing passes 4.5:1.">
      <div className="seg" role="tablist" aria-label="Theme">
        {['light', 'dark'].map((m) => <button key={m} role="tab" aria-selected={mode === m} onClick={() => setMode(m)}>{m === 'light' ? 'Light' : 'Dark'}</button>)}
      </div>
      <div className="swatches">
        {tokens.color.tokens.map((t, i) => (
          <button key={t.name} className="swatch" data-reveal style={{ '--d': (i % 6) * 30 + 'ms' }}
            onClick={(e) => { copy('Color.' + swiftName(t.name)); const el = e.currentTarget; el.classList.add('copied'); setTimeout(() => el.classList.remove('copied'), 1100); }}>
            <span className="chip" style={{ background: val(t) }} />
            <b>{t.name}</b>
            <code>{val(t)}</code>
            <em>Copied Color.{swiftName(t.name)}</em>
          </button>
        ))}
      </div>
    </Section>
  );
}

function Type() {
  return (
    <Section id="type" eyebrow="Foundations" title="Typography" lead="Plus Jakarta Sans, mapped to iOS text styles so it scales with Dynamic Type.">
      <div className="types">
        {TYPE.map(([cls, sample, figma, size, weight, code]) => (
          <div key={cls} className="type-row" data-reveal>
            <div className={'type-sample ' + cls}>{sample}</div>
            <div className="type-meta">
              <div className="tags"><span>{size}</span><span>{weight}</span><span>.{cls === 'large-title' ? 'largeTitle' : cls}</span></div>
              <CodeBlock code={code} />
              <CopyChip text={'Cashout/' + figma} label={'Figma · Cashout/' + figma} />
            </div>
          </div>
        ))}
      </div>
    </Section>
  );
}

function Components() {
  const cards = [
    ['Button', 'Filled for the one primary action, plain for the way out.', <div className="stack" key="b"><C.Button fullWidth>Cash out</C.Button><C.Button variant="plain">Keep playing</C.Button></div>],
    ['AmountHero', 'Green means money, navy means waiting.', <C.AmountHero key="h" className="co-mini" amount={2.81}><C.Pill glass /></C.AmountHero>],
    ['Countdown', 'h:mm:ss with rolling digits.', <div key="c" style={{ width: 260 }}><C.Countdown size="card" seconds={11643} live /></div>],
    ['InfoRow', 'When stars turn into rewards.', <div key="i" style={{ width: 320 }}><C.InfoRow secondsLeft={13500} /></div>],
    ['HistoryList', 'Status is text plus color.', <div key="l" style={{ width: 320 }}><C.HistoryList items={[{ date: 'April 26', amount: 1.3 }, { date: 'March 22', amount: 0.86, status: 'pending' }, { date: 'March 14', amount: 1.12, status: 'failed' }]} /></div>],
    ['InlineMessage', 'Limits and errors, always with an icon.', <div key="m" style={{ width: 320 }}><C.InlineMessage>You’ve reached the maximum balance. Cash out to keep earning.</C.InlineMessage></div>],
    ['Pill', 'Small capsule shortcut with a 44pt tap area.', <C.Pill key="p" />],
    ['StatTile', 'Balances on Home.', <div key="s" style={{ width: 200, display: 'flex' }}><C.StatTile icon="star" label="Game coins" value="66,378" /></div>]
  ];
  return (
    <Section id="components" eyebrow="Library" title="Components" lead="Live, tappable versions of the SwiftUI views. Copy the code under each.">
      <div className="cards">
        {cards.map(([name, sub, el], i) => (
          <article key={name} className="card" data-reveal style={{ '--d': (i % 3) * 60 + 'ms' }}>
            <div className="card-stage">{el}</div>
            <div className="card-body">
              <h3>{name}</h3>
              <p>{sub}</p>
              <CodeBlock code={SNIPPETS[name]} />
            </div>
          </article>
        ))}
      </div>
    </Section>
  );
}

function CountUpDemo() {
  const [v, setV] = useState(0);
  const [k, setK] = useState(0);
  useEffect(() => {
    let raf, t0;
    const to = k % 2 ? 0 : 2.81, from = k % 2 ? 2.81 : 0;
    const f = (ts) => { if (!t0) t0 = ts; const p = Math.min(1, (ts - t0) / 600); setV(from + (to - from) * (1 - Math.pow(1 - p, 3))); if (p < 1) raf = requestAnimationFrame(f); };
    raf = requestAnimationFrame(f);
    return () => cancelAnimationFrame(raf);
  }, [k]);
  return <div className="demo-col"><C.AmountHero className="co-mini" amount={v} /><button className="replay" onClick={() => setK(k + 1)}>↻ Replay</button></div>;
}
function SuccessDemo() {
  const [on, setOn] = useState(false);
  return (
    <div className="demo-col">
      <div key={String(on)} className={on ? 'co-anim-pop' : 'co-anim-fade'}><C.AmountHero className="co-mini" state={on ? 'success' : 'earned'} amount={on ? 2.81 : 0.32} /></div>
      <button className="replay" onClick={() => setOn(!on)}>{on ? '↻ Reset' : '▶ Cash out'}</button>
    </div>
  );
}
function RevealDemo() {
  const [k, setK] = useState(0);
  return (
    <div className="demo-col">
      <div key={k} className="demo-reveal">
        {[<C.InfoRow key="a" secondsLeft={13500} />, <C.Button key="b" fullWidth>Cash out</C.Button>, <C.Button key="c" variant="plain">Keep playing</C.Button>].map((el, i) => (
          <div key={i} className="co-anim-rise" style={{ animationDelay: i * 50 + 'ms' }}>{el}</div>
        ))}
      </div>
      <button className="replay" onClick={() => setK(k + 1)}>↻ Replay</button>
    </div>
  );
}

function Motion() {
  const demos = {
    press: <div className="demo-col"><C.Button style={{ width: 240 }}>Press and hold</C.Button><C.Pill /></div>,
    count: <CountUpDemo />,
    success: <SuccessDemo />,
    tick: <div style={{ width: 260 }}><C.Countdown size="card" seconds={11643} live /></div>,
    reveal: <RevealDemo />
  };
  return (
    <Section id="motion" eyebrow="Motion" title="Animations and transitions" lead="System springs, mirrored on the web. With Reduce Motion on, every move becomes a crossfade." dark>
      <div className="motion-grid">
        {Object.entries(MOTION).map(([key, m], i) => (
          <article key={key} className="motion-card" data-reveal style={{ '--d': (i % 3) * 60 + 'ms' }}>
            <div className="motion-stage">{demos[key]}</div>
            <div className="motion-body">
              <h3>{m.title}</h3>
              <div className="tags">{m.tokens.map((t) => <span key={t}>{t}</span>)}</div>
              <CodeBlock code={m.code} />
            </div>
          </article>
        ))}
      </div>
    </Section>
  );
}

function Prototype() {
  const src = BASE + 'prototype/index.html';
  return (
    <Section id="prototype" eyebrow="Prototype" title="Try the cash-out flow" lead="Home, the sheet, History, cashing out, success and the wait timer, all clickable.">
      <div className="proto" data-reveal>
        <iframe title="Cashout prototype" src={src} loading="lazy" />
      </div>
      <p className="proto-link"><a href={src} target="_blank" rel="noreferrer">Open the prototype on its own page ↗</a></p>
    </Section>
  );
}

function Footer() {
  return (
    <footer className="footer">
      <div className="wrap footer-in">
        <span className="brand">Cashout iOS</span>
        <div className="navlinks">
          <a href={LINKS.figma} target="_blank" rel="noreferrer">Figma file ↗</a>
          <a href={LINKS.repo} target="_blank" rel="noreferrer">GitHub ↗</a>
        </div>
      </div>
    </footer>
  );
}

export default function App() {
  useReveal();
  return (
    <>
      <Hero />
      <main>
        <Rules />
        <Colors />
        <Type />
        <Components />
        <Motion />
        <Prototype />
      </main>
      <Footer />
    </>
  );
}
