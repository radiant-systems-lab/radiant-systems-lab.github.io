
// index page Research Areas - click and show
const index_researchAreas = [
  {
    title: 'Reproducible and Accountable Systems (RAS)',
    description: 'Improving data-intensive distributed and parallel science workflows with reproducible and accountable containers',
  },
  {
    title: 'Transparent and Explainable AI (XAI)',
    description: 'Make data, algorithms, and decision-making processes in science workflows explainable and understandable.',
  },
  {
    title: 'Infrastructure and Policy (RIP)',
    description: 'Engage in resource and systems optimization of infrastructure, guided by policy frameworks.',
  },
  {
    title: 'Big Data Management',
    description: 'Optimizing scientific data for volume, velocity, and variety via indexing, streaming, and semantic dataspaces.',
  },
  {
    title: 'Scalable Cyberinfrastructure',
    description: 'Enables scientific research and innovation at scale by supporting advanced research through distributed, collaborative, and data-intensive capabilities.',
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
