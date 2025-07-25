
// index page Research Areas - click and show
const index_researchAreas = [
  {
    title: 'Machine Learning',
    description: 'Developing algorithms that allow computers to learn patterns from data and make predictions or decisions.',
  },
  {
    title: 'Computer Vision',
    description: 'Enabling machines to interpret and process visual data from the world.',
  },
  {
    title: 'Natural Language Processing',
    description: 'Teaching computers to understand and generate human language.',
  },
  {
    title: 'Cybersecurity',
    description: 'Protecting systems and networks from digital attacks.',
  },
  {
    title: 'Human-Computer Interaction',
    description: 'Designing intuitive interfaces that improve the way humans interact with technology.',
  },
  {
    title: 'Distributed Systems',
    description: 'Studying systems whose components are located on different networked computers.',
  },
];

const accordionContainer = document.querySelector('#index_research_areas .accordion');

index_researchAreas.forEach((area, index) => {
  const item = document.createElement('div');
  item.classList.add('accordion-item');

  const header = document.createElement('div');
  header.classList.add('accordion-header');
  header.textContent = area.title;

  const symbol = document.createElement('span');
  symbol.textContent = '+';
  header.appendChild(symbol);

  const body = document.createElement('div');
  body.classList.add('accordion-body');
  body.textContent = area.description;

  header.addEventListener('click', () => {
    const isOpen = header.classList.contains('open');
    document.querySelectorAll('.accordion-header').forEach(h => {
      h.classList.remove('open');
      h.querySelector('span').textContent = '+';
    });
    document.querySelectorAll('.accordion-body').forEach(b => b.classList.remove('open'));

    if (!isOpen) {
      header.classList.add('open');
      body.classList.add('open');
      symbol.textContent = '−';
    }
  });

  item.appendChild(header);
  item.appendChild(body);
  accordionContainer.appendChild(item);
});
