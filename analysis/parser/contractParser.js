const fs = require("fs");

function parseContract(sourceCode) {
  const functions = [];

  // 1. ищем функции
  const functionRegex = /function\s+(\w+)\s*\((.*?)\)\s*(public|private|internal|external)?\s*(.*)?\{/g;

  let match;

  while ((match = functionRegex.exec(sourceCode)) !== null) {
    const name = match[1];
    const visibility = match[3] || "unknown";
    const modifiers = match[4] || "";

    functions.push({
      name,
      visibility,
      modifiers: modifiers.trim(),
      risky_patterns: {
        has_external_call: /call\.value|\.call\(|transfer\(/.test(sourceCode),
        has_require: sourceCode.includes("require"),
      }
    });
  }

  // 2. ищем onlyOwner / access control
  const authIssues = [];

  const mintFunctions = sourceCode.match(/function\s+mint/g) || [];

  if (mintFunctions.length > 0 && !sourceCode.includes("onlyOwner")) {
    authIssues.push({
      issue: "Missing access control",
      severity_hint: "high"
    });
  }

  return {
    functions,
    authIssues
  };
}

// test run
const code = fs.readFileSync("./contracts/SecureVault.sol", "utf-8");

console.log(JSON.stringify(parseContract(code), null, 2));
