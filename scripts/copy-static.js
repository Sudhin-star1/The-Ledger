/**
 * Copy static HTML/JS into dist/ so Vercel serves them (avoids Python-only detection).
 */
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const dist = path.join(root, "dist");

const files = [
  "index.html",
  "actual.html",
  "api-config.js",
  "api-config.example.js",
  "gemini-test.html",
  "next.html",
];

fs.mkdirSync(dist, { recursive: true });
for (const name of files) {
  const src = path.join(root, name);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, path.join(dist, name));
  }
}
console.log("Static files copied to dist/");
