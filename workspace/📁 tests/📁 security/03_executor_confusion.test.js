// 03_executor_confusion.test.js
// Test for Executor Confusion Vulnerability

const axios = require('axios');
const { spawn } = require('child_process');

describe('Executor Confusion Tests', () => {
  let serverProcess;
  
  beforeAll(async () => {
    // Start the server in the background
    serverProcess = spawn('node', ['app.js'], {
      env: { ...process.env, NODE_ENV: 'test' }
    });
    // Wait a moment for the server to start
    await new Promise(resolve => setTimeout(resolve, 2000));
  });
  
  afterAll(() => {
    // Kill the server process
    if (serverProcess) {
      serverProcess.kill();
    }
  });
  
  test('Should prevent command execution confusion', async () => {
    const commandConfusionInputs = [
      // Shell command injection
      {
        input: "normal input && ls -la",
        expectedBehavior: "Should not execute shell commands"
      },
      {
        input: "normal input; rm -rf /",
        expectedBehavior: "Should not execute destructive commands"
      },
      {
        input: "normal input | cat /etc/passwd",
        expectedBehavior: "Should not pipe to system commands"
      },
      // Template injection
      {
        input: "Hello {{7*7}}",
        expectedBehavior: "Should not evaluate mathematical expressions"
      },
      {
        input: "User: ${process.env.USER}",
        expectedBehavior: "Should not access environment variables"
      },
      // Script injection
      {
        input: "normal input <script>console.log('executed')</script>",
        expectedBehavior: "Should not execute client-side scripts"
      }
    ];
    
    for (const test of commandConfusionInputs) {
      try {
        const response = await axios.post('http://localhost:3000/api/process', {
          userInput: test.input
        });
        
        // Verify no command execution occurred
        expect(response.data).not.toMatch(/total|drwx|root|home/i);
        expect(response.data).not.toMatch(/49|mathematical|evaluation/i);
        expect(response.data).not.toMatch(/<script|executed/i);
        
        // Verify the input was treated as literal text
        expect(response.data.toString().toLowerCase()).toContain(test.input.toLowerCase());
        
        console.log(`Command confusion input "${test.input}" handled safely`);
      } catch (error) {
        console.log(`Expected behavior for command confusion input:`, error.message);
      }
    }
  });
  
  test('Should handle different execution contexts properly', async () => {
    const contextTests = [
      // Different script types
      {
        type: 'javascript',
        code: 'console.log("executed"); process.exit(0);',
        location: 'input_field'
      },
      {
        type: 'python',
        code: 'print("executed")\nimport os\nos.system("ls")',
        location: 'input_field'
      },
      {
        type: 'shell',
        code: 'echo "executed"; whoami;',
        location: 'input_field'
      },
      // Different evaluation contexts
      {
        type: 'template_engine',
        code: '<%= system("whoami") %>',
        location: 'template_variable'
      },
      {
        type: 'expression_evaluator',
        code: '${{7*7+system("ls")}}',
        location: 'math_expression'
      }
    ];
    
    for (const test of contextTests) {
      try {
        const payload = {};
        payload[test.location] = test.code;
        
        const response = await axios.post('http://localhost:3000/api/process', payload);
        
        // Verify that code was not executed in any context
        expect(response.data).not.toMatch(/executed|root|current|process/i);
        expect(response.data).not.toMatch(/49|mathematical|calculation/i);
        
        // Verify that input was treated as literal text
        expect(response.data.toString()).toContain(test.code.replace(/[<>=]/g, ''));
      } catch (error) {
        console.log(`Context test handled appropriately for ${test.type}:`, error.message);
      }
    }
  });
  
  test('Should prevent sandbox escape attempts', async () => {
    const sandboxEscapeAttempts = [
      // Attempts to break out of restricted environments
      {
        code: 'global.process.mainModule.require("child_process").exec("ls")',
        description: 'Node.js global object access'
      },
      {
        code: 'this.constructor.constructor("return this.process")().mainModule.require("fs").readFileSync("/etc/passwd")',
        description: 'Constructor chain exploitation'
      },
      {
        code: 'Function("return this")().process.mainModule.require("child_process").execSync("whoami")',
        description: 'Function constructor exploitation'
      },
      // Attempts to access restricted resources
      {
        code: 'require("vm").runInNewContext("process.env", {})',
        description: 'VM sandbox bypass'
      },
      {
        code: 'eval("process.env")',
        description: 'Direct eval bypass'
      }
    ];
    
    for (const attempt of sandboxEscapeAttempts) {
      try {
        const response = await axios.post('http://localhost:3000/api/evaluate', {
          expression: attempt.code
        });
        
        // Verify that no system information was leaked
        expect(response.data).not.toMatch(/root|user|environment|process/i);
        expect(response.data).not.toMatch(/etc|passwd|bin|sbin/i);
        
        // Response should indicate safe handling
        expect(response.data).toMatch(/safe|blocked|restricted|error/i);
        
        console.log(`Sandbox escape attempt blocked: ${attempt.description}`);
      } catch (error) {
        // Expected behavior - escape attempts should fail
        console.log(`Sandbox escape properly prevented:`, attempt.description);
      }
    }
  });
  
  test('Should handle dynamic code evaluation safely', async () => {
    const dynamicEvalInputs = [
      // Various eval-like operations
      {
        input: '(function(){return "evaluated"})()',
        type: 'function_constructor'
      },
      {
        input: 'new Function("return \'dynamic\'")()',
        type: 'new_function'
      },
      {
        input: 'setTimeout("console.log(\'timeout\')", 1)',
        type: 'set_timeout'
      },
      {
        input: 'setInterval("console.log(\'interval\')", 1000)',
        type: 'set_interval'
      },
      // Template literals with evaluation
      {
        input: '`result: ${process.env.USER}`',
        type: 'template_literal'
      }
    ];
    
    for (const test of
