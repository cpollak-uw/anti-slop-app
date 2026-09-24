"""Accessibility patches for Streamlit's own markup.

Streamlit renders its sidebar in a way that trips three axe-core rules: the sidebar
carries aria-expanded on an element whose role doesn't allow it, the navigation list
holds section headers as direct children of a <ul>, and neither the sidebar nor the
main area is marked as a landmark, so a screen reader can't jump between them.

None of that is reachable from Python or CSS, so this module injects a small script
through a zero-height component. The script runs in an iframe written with srcdoc,
which shares the page's origin, so it can adjust the parent document. It fixes roles
only and never moves or deletes an element, so React keeps control of the DOM.
"""

import streamlit.components.v1 as components

_SCRIPT = """
<script>
const doc = window.parent.document;

function patch() {
  // 1. The sidebar is a <section> with aria-expanded, which that role does not allow.
  //    Naming it a navigation landmark makes the attribute valid and gives screen
  //    reader users a "navigation" region to jump to.
  const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
  if (sidebar && sidebar.getAttribute('role') !== 'navigation') {
    sidebar.setAttribute('role', 'navigation');
    sidebar.setAttribute('aria-label', 'Course pages');
  }

  // 2. The page list is a <ul> whose direct children include section headers
  //    ("Start here", "Course units"). Marking them as list items keeps the list
  //    valid, and the pages inside stay reachable as list items.
  doc.querySelectorAll('ul[data-testid="stSidebarNavItems"]').forEach(ul => {
    // The <ul> mixes section headers with <div> wrappers that each hold the <li>
    // links. Dropping the list role from the outer <ul> and giving each wrapper a
    // list role puts every <li> inside a real list, which is what a screen reader
    // needs in order to announce "list, 3 items".
    ul.setAttribute('role', 'none');
    [...ul.children].forEach(child => {
      if (child.tagName === 'DIV' && child.querySelector('li')) {
        child.setAttribute('role', 'list');
      }
    });
  });

  // 3. The page content itself sits in an unlabelled <section>. Without a main
  //    landmark, a screen reader has no way to skip the navigation.
  const main = doc.querySelector('section[data-testid="stMain"]');
  if (main && main.getAttribute('role') !== 'main') {
    main.setAttribute('role', 'main');
    main.setAttribute('aria-label', 'Page content');
  }

  // 4. The component's own iframe is decorative and should not be announced.
  doc.querySelectorAll('iframe[title="streamlit_component"], .stCustomComponentV1')
     .forEach(f => { f.setAttribute('aria-hidden', 'true'); f.setAttribute('tabindex', '-1'); });
}

patch();
// Streamlit rebuilds parts of the page as students answer questions, so re-apply.
new MutationObserver(patch).observe(doc.body, {childList: true, subtree: true});
</script>
"""


def patch_streamlit_a11y():
    components.html(_SCRIPT, height=0, width=0)
