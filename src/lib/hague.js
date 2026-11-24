import countries from '../data/hague-countries.json';
export const SITE = 'https://apostillesteps.com';
export const STATUS_URL = 'https://www.hcch.net/en/instruments/conventions/status-table/?cid=41';
export const US_AUTH_URL = 'https://www.hcch.net/en/states/authorities/details3/?aid=353';
export const US_EIF = '1981-10-15';
export const CHECKED = '2026-11-23';
const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
export function fmt(iso) {
  if (!iso) return '—';
  const [y, m, d] = iso.split('-').map(Number);
  return `${MONTHS[m - 1]} ${d}, ${y}`;
}
export const sorted = [...countries].sort((a, b) => a.name.localeCompare(b.name));

// How the Convention stands between this country and the United States, from the HCCH status table and notification pages.
export function usRelation(c) {
  if (!c.in_force) return { ok: false, short: `Not yet (from ${fmt(c.entry_into_force)})`, text: `Not yet. The HCCH status table gives ${fmt(c.entry_into_force)} as the date the Convention enters into force for ${c.name}. Until then, a U.S. document going to ${c.name} follows the authentication and legalization route instead of an apostille.` };
  if (c.slug === 'liberia') return { ok: true, short: 'Yes, since May 20, 2015', text: 'Yes, since May 20, 2015. The United States objected to Liberia’s accession in 1995 and withdrew the objection on May 20, 2015; the HCCH notification page says the Convention entered into force between Liberia and the United States on that date.' };
  if (c.slug === 'kosovo') return { ok: true, short: 'Yes', text: 'Yes. The HCCH notification page lists the Contracting States between which the Convention does not apply with Kosovo, and the United States is not one of them. The United States did file a formal declaration about Kosovo’s accession (dated September 6, 2017); the full text is on the depositary’s site linked from the HCCH page.' };
  if (c.us_in_objection_notes === 'not_named') return { ok: true, short: 'Yes', text: `Yes. Some Contracting States objected to ${c.name}’s accession, so the Convention does not apply between ${c.name} and those States. The United States is not among the objecting States on the HCCH notification page.` };
  return { ok: true, short: 'Yes', text: `Yes. Both ${c.name} and the United States are Contracting Parties, and the Convention has been in force for the United States since ${fmt(US_EIF)}.` };
}
export const GUIDES = [
  ['New York', '/new-york-apostille/'], ['California', '/california-apostille/'], ['Texas', '/texas-apostille/'], ['Florida', '/florida-apostille/'],
  ['Massachusetts', '/massachusetts-apostille/'], ['New Jersey', '/new-jersey-apostille/'], ['Virginia', '/virginia-apostille/'], ['North Carolina', '/north-carolina-apostille/'],
];
