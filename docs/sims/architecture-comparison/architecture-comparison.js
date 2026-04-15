// Three Retrieval Architecture Comparison
// CANVAS_HEIGHT: 520
// Shows RAG, GraphRAG, and CKG pipelines with hover tooltips

let canvasWidth = 900;
let canvasHeight = 520;
let margin = 20;

// Pipeline definitions: label, color, steps with descriptions
let pipelines = [
  {
    label: 'RAG',
    color: [66, 133, 244],  // Blue
    steps: [
      {
        name: 'MkDocs\nText',
        desc: 'Source documents are MkDocs Markdown chapters from the intelligent textbook. Each chapter contains 3,000-8,000 words of educational content covering domain concepts.'
      },
      {
        name: 'Chunking',
        desc: 'Text is split into 512-token chunks with 50-token overlap. This fixed-size windowing discards document structure and can split concepts across chunk boundaries.'
      },
      {
        name: 'Embed-\ndings',
        desc: 'Each chunk is converted to a dense vector using text-embedding-3-small. These embeddings capture semantic similarity but lose explicit structural relationships between concepts.'
      },
      {
        name: 'Top-k\nRetrieval',
        desc: 'The query is embedded and the 5 nearest chunks are retrieved via FAISS L2 search. This returns 2,560 tokens of context, much of which is off-topic noise from unrelated sentences.'
      },
      {
        name: 'LLM\n(Claude)',
        desc: 'Claude Sonnet receives the query plus 5 retrieved chunks as context. Total prompt is typically 3,000-5,000 tokens. The LLM must infer relationships that were lost during chunking.'
      }
    ]
  },
  {
    label: 'GraphRAG',
    color: [142, 68, 173],  // Purple
    steps: [
      {
        name: 'MkDocs\nText',
        desc: 'Same MkDocs Markdown chapters used by RAG. GraphRAG processes the full text to extract entities and relationships, rather than chunking it into fixed-size windows.'
      },
      {
        name: 'Entity\nExtraction',
        desc: 'An LLM pass extracts named entities and relationships from the text. This is the most expensive step — it consumes thousands of tokens per chapter and can hallucinate edges not in the source material.'
      },
      {
        name: 'Graph\nBuilding',
        desc: 'Extracted entities become nodes and relationships become edges in a property graph. Community detection groups related concepts into clusters for summarization. Build cost is HIGH.'
      },
      {
        name: 'Community\nSearch',
        desc: 'Queries are matched to relevant graph communities. Local search handles entity queries; global search handles category queries. Token cost varies widely (2,000-8,000 per query).'
      },
      {
        name: 'LLM\n(Claude)',
        desc: 'Claude Sonnet receives the query plus community summaries as context. Better than RAG on multi-hop queries because graph structure is preserved, but dynamic extraction introduces noise.'
      }
    ]
  },
  {
    label: 'CKG',
    color: [39, 174, 96],  // Green
    steps: [
      {
        name: 'CSV\nFile',
        desc: 'A pre-structured learning-graph.csv with 4 columns: ConceptID, ConceptLabel, Dependencies, TaxonomyID. This is the canonical knowledge representation — zero build cost, zero ambiguity.'
      },
      {
        name: 'Concept\nLookup',
        desc: 'The query concept is matched to a node by exact label match in the CSV. This is a simple string lookup — no embedding, no LLM call, no approximation. Deterministic and instant.'
      },
      {
        name: 'DAG\nTraversal',
        desc: 'BFS for 1-hop dependency queries (T2), DFS for multi-hop path queries (T3), and taxonomy filter for category queries (T4). Explicit edges mean zero inference errors on structural queries.'
      },
      {
        name: 'Subgraph\nExtraction',
        desc: 'The matched concept plus its direct neighbors and connecting edges are serialized as context. Typically 80-150 tokens — near-zero noise because every token is structurally relevant.'
      },
      {
        name: 'LLM\n(Claude)',
        desc: 'Claude Sonnet receives the query plus a tiny, precise subgraph as context. Total prompt is only 150-400 tokens — a 13x reduction vs RAG. Hallucination rate is zero by construction.'
      }
    ]
  }
];

let hoveredStep = null;
let tooltipAlpha = 0;

function setup() {
  updateCanvasSize();
  let canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));
  textAlign(CENTER, CENTER);
  textFont('Arial');
}

function updateCanvasSize() {
  let containerWidth = min(windowWidth - 10, 1000);
  canvasWidth = max(containerWidth, 600);
}

function draw() {
  background(252, 252, 252);

  // Title
  fill(30);
  noStroke();
  textSize(18);
  textStyle(BOLD);
  text('Three Knowledge Retrieval Architectures', canvasWidth / 2, 22);
  textSize(12);
  textStyle(NORMAL);
  fill(100);
  text('Hover over any component to learn more', canvasWidth / 2, 42);

  let pipelineHeight = 110;
  let startY = 65;
  let labelWidth = 85;
  let stepAreaWidth = canvasWidth - labelWidth - margin * 2 - 10;

  hoveredStep = null;

  for (let p = 0; p < pipelines.length; p++) {
    let pipeline = pipelines[p];
    let py = startY + p * (pipelineHeight + 10);
    let nSteps = pipeline.steps.length;
    let stepWidth = stepAreaWidth / nSteps;
    let boxWidth = stepWidth * 0.7;
    let boxHeight = 60;
    let boxY = py + (pipelineHeight - boxHeight) / 2;

    // Pipeline background
    fill(pipeline.color[0], pipeline.color[1], pipeline.color[2], 15);
    stroke(pipeline.color[0], pipeline.color[1], pipeline.color[2], 60);
    strokeWeight(1);
    rect(margin, py, canvasWidth - margin * 2, pipelineHeight, 8);

    // Pipeline label
    fill(pipeline.color[0], pipeline.color[1], pipeline.color[2]);
    noStroke();
    textSize(16);
    textStyle(BOLD);
    text(pipeline.label, margin + labelWidth / 2, py + pipelineHeight / 2);

    // Draw steps
    for (let s = 0; s < nSteps; s++) {
      let sx = labelWidth + margin + s * stepWidth + stepWidth / 2;
      let boxLeft = sx - boxWidth / 2;

      // Check hover
      let isHovered = mouseX > boxLeft && mouseX < boxLeft + boxWidth &&
                      mouseY > boxY && mouseY < boxY + boxHeight;

      if (isHovered) {
        hoveredStep = { pipeline: p, step: s, x: sx, y: boxY };
      }

      // Box shadow on hover
      if (isHovered) {
        fill(pipeline.color[0], pipeline.color[1], pipeline.color[2], 30);
        noStroke();
        rect(boxLeft - 2, boxY - 2, boxWidth + 4, boxHeight + 4, 8);
      }

      // Box
      fill(255);
      stroke(pipeline.color[0], pipeline.color[1], pipeline.color[2]);
      strokeWeight(isHovered ? 3 : 1.5);
      rect(boxLeft, boxY, boxWidth, boxHeight, 6);

      // Label
      fill(40);
      noStroke();
      textSize(11);
      textStyle(BOLD);
      let lines = pipeline.steps[s].name.split('\n');
      if (lines.length === 1) {
        text(lines[0], sx, boxY + boxHeight / 2);
      } else {
        text(lines[0], sx, boxY + boxHeight / 2 - 8);
        text(lines[1], sx, boxY + boxHeight / 2 + 8);
      }

      // Arrow to next step
      if (s < nSteps - 1) {
        let arrowStartX = boxLeft + boxWidth + 2;
        let arrowEndX = labelWidth + margin + (s + 1) * stepWidth + stepWidth / 2 - boxWidth / 2 - 2;
        let arrowY = boxY + boxHeight / 2;
        stroke(pipeline.color[0], pipeline.color[1], pipeline.color[2], 150);
        strokeWeight(2);
        line(arrowStartX, arrowY, arrowEndX - 6, arrowY);
        // Arrowhead
        fill(pipeline.color[0], pipeline.color[1], pipeline.color[2], 150);
        noStroke();
        triangle(arrowEndX, arrowY, arrowEndX - 8, arrowY - 4, arrowEndX - 8, arrowY + 4);
      }
    }
  }

  // Token cost summary bar at bottom
  let barY = startY + 3 * (pipelineHeight + 10) + 5;
  fill(30);
  noStroke();
  textSize(13);
  textStyle(BOLD);
  textAlign(LEFT, CENTER);
  text('Tokens per query:', margin + 10, barY + 12);

  let barStartX = margin + 160;
  let barMaxWidth = canvasWidth - barStartX - margin - 60;

  // RAG bar
  let ragWidth = barMaxWidth * (4000 / 5000);
  fill(66, 133, 244, 180);
  rect(barStartX, barY, ragWidth, 20, 3);
  fill(255);
  textSize(11);
  textStyle(BOLD);
  text('RAG: ~4,000', barStartX + 8, barY + 10);

  // GraphRAG bar
  let gragWidth = barMaxWidth;
  fill(142, 68, 173, 180);
  rect(barStartX, barY + 24, gragWidth, 20, 3);
  fill(255);
  text('GraphRAG: ~5,000', barStartX + 8, barY + 34);

  // CKG bar
  let ckgWidth = barMaxWidth * (300 / 5000);
  fill(39, 174, 96, 180);
  rect(barStartX, barY + 48, ckgWidth, 20, 3);
  fill(255);
  textSize(10);
  text('CKG: ~300', barStartX + 8, barY + 58);

  // 13x label
  fill(39, 174, 96);
  textSize(12);
  textStyle(BOLD);
  textAlign(LEFT, CENTER);
  text('13x fewer', barStartX + ckgWidth + 10, barY + 58);

  textAlign(CENTER, CENTER);

  // Draw tooltip last (on top)
  if (hoveredStep !== null) {
    drawTooltip();
  }
}

function drawTooltip() {
  let step = pipelines[hoveredStep.pipeline].steps[hoveredStep.step];
  let desc = step.desc;
  let col = pipelines[hoveredStep.pipeline].color;

  // Tooltip dimensions
  let tooltipWidth = 280;
  let padding = 12;
  let lineHeight = 16;

  // Word wrap
  textSize(12);
  textStyle(NORMAL);
  let words = desc.split(' ');
  let wrappedLines = [];
  let currentLine = '';
  for (let w of words) {
    let testLine = currentLine ? currentLine + ' ' + w : w;
    if (textWidth(testLine) > tooltipWidth - padding * 2) {
      wrappedLines.push(currentLine);
      currentLine = w;
    } else {
      currentLine = testLine;
    }
  }
  if (currentLine) wrappedLines.push(currentLine);

  let tooltipHeight = wrappedLines.length * lineHeight + padding * 2 + 4;

  // Position tooltip
  let tx = hoveredStep.x - tooltipWidth / 2;
  let ty = hoveredStep.y - tooltipHeight - 8;

  // Keep on screen
  if (tx < 5) tx = 5;
  if (tx + tooltipWidth > canvasWidth - 5) tx = canvasWidth - tooltipWidth - 5;
  if (ty < 5) ty = hoveredStep.y + 68;

  // Shadow
  fill(0, 0, 0, 30);
  noStroke();
  rect(tx + 3, ty + 3, tooltipWidth, tooltipHeight, 6);

  // Background
  fill(255, 255, 255, 245);
  stroke(col[0], col[1], col[2]);
  strokeWeight(2);
  rect(tx, ty, tooltipWidth, tooltipHeight, 6);

  // Text
  fill(40);
  noStroke();
  textSize(12);
  textStyle(NORMAL);
  textAlign(LEFT, TOP);
  for (let i = 0; i < wrappedLines.length; i++) {
    text(wrappedLines[i], tx + padding, ty + padding + i * lineHeight);
  }
  textAlign(CENTER, CENTER);
}

function windowResized() {
  updateCanvasSize();
  resizeCanvas(canvasWidth, canvasHeight);
}
