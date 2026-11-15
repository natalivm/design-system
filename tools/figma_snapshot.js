// Run in the Figma file (use_figma, or the console of a development plugin) to take a snapshot of the
// design system: every Cashout/* variable resolved per mode, with its web code name, and every
// Cashout/* text style. Save the returned JSON as figma/snapshot.json, then run tools/figma_sync.py.
const cols = (await figma.variables.getLocalVariableCollectionsAsync()).filter(c => c.name.startsWith('Cashout/'));
const all = await figma.variables.getLocalVariablesAsync();
const byId = Object.fromEntries(all.map(v => [v.id, v]));
const hex = c => '#' + [c.r, c.g, c.b].map(x => Math.round(x * 255).toString(16).padStart(2, '0')).join('') + (c.a !== undefined && c.a < 1 ? Math.round(c.a * 255).toString(16).padStart(2, '0') : '');
function resolve(v, modeId, depth) {
  let val = v.valuesByMode[modeId];
  if (val === undefined) val = v.valuesByMode[Object.keys(v.valuesByMode)[0]];
  if (val && val.type === 'VARIABLE_ALIAS') {
    const t = byId[val.id]; if (!t || depth > 5) return null;
    return resolve(t, t.valuesByMode[modeId] !== undefined ? modeId : Object.keys(t.valuesByMode)[0], depth + 1);
  }
  return v.resolvedType === 'COLOR' ? hex(val) : val;
}
const snap = { file: figma.fileKey, collections: {} };
for (const c of cols) {
  snap.collections[c.name] = {
    modes: c.modes.map(m => m.name),
    vars: all.filter(v => v.variableCollectionId === c.id).map(v => {
      const o = { name: v.name, type: v.resolvedType, web: (v.codeSyntax && v.codeSyntax.WEB) || null, description: v.description || '', values: {} };
      for (const m of c.modes) o.values[m.name] = resolve(v, m.modeId, 0);
      return o;
    })
  };
}
snap.textStyles = (await figma.getLocalTextStylesAsync()).filter(s => s.name.startsWith('Cashout/')).map(s => ({
  name: s.name, family: s.fontName.family, style: s.fontName.style, size: s.fontSize,
  lineHeight: s.lineHeight.unit === 'PIXELS' ? s.lineHeight.value : s.lineHeight.unit,
  letterSpacing: s.letterSpacing.value ? s.letterSpacing.value + (s.letterSpacing.unit === 'PERCENT' ? '%' : 'px') : 0
}));
return snap;
