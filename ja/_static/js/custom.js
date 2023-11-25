const classes = document.getElementsByClassName('class')
const tables = document.getElementsByClassName('py-attribute-table')



for (const [i, _class] of Object.entries(classes)) {
    const sig = _class.getElementsByTagName('dt').item(0);
    const table = Object.entries(tables).filter((table) => table[1].getAttribute('data-move-to-id') == sig.id)[0];
    sig.classList.add(`class-sig-${i}`);
    table.id = `attributable-${i}`;
    sig.parentNode.insertBefore(table[1], sig.nextSibling)
}