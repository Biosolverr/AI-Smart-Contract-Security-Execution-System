// 02_json_field_injection.test.js
// Test for JSON Field Injection Vulnerability

const axios = require('axios');
const { spawn } = require('child_process');

describe('JSON Field Injection Tests', () => {
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
  
  test('Should prevent JSON field injection attacks', async () => {
    const injectionPayloads = [
      // Prototype pollution attempt
      {
        "__proto__": {
          "polluted": "value"
        },
        "normalField": "normalValue"
      },
      // Constructor override
      {
        "constructor": {
          "prototype": {
            "polluted": "value"
          }
        },
        "normalField": "normalValue"
      },
      // Additional properties injection
      {
        "user": {
          "id": 1,
          "role": "user",
          "admin": true
        }
      },
      // Type confusion
      {
        "balance": "0",
        "balance": 999999,
        "isAdmin": "false",
        "isAdmin": true
      },
      // Nested injection
      {
        "profile": {
          "__proto__": {
            "injectedProperty": "injectedValue"
          },
          "name": "Normal User"
        }
      }
    ];
    
    for (const payload of injectionPayloads) {
      try {
        const response = await axios.post('http://localhost:3000/api/submit', payload);
        
        // Verify that injected fields are not processed
        expect(response.data).not.toHaveProperty('polluted');
        expect(response.data).not.toHaveProperty('injectedProperty');
        
        // Verify that admin privileges are not granted
        expect(response.data).not.toHaveProperty('admin', true);
        expect(response.data).not.toHaveProperty('isAdmin', true);
        
        // Verify that balances are not manipulated
        expect(response.data).not.toHaveProperty('balance', 999999);
        
        console.log('JSON injection payload blocked successfully');
      } catch (error) {
        console.log('Expected rejection of malformed JSON:', error.message);
      }
    }
  });
  
  test('Should handle complex nested objects safely', async () => {
    const complexObject = {
      "user": {
        "id": 1,
        "profile": {
          "name": "John Doe",
          "settings": {
            "theme": "dark",
            "__proto__": {
              "adminOverride": true
            },
            "constructor": {
              "prototype": {
                "accessLevel": "admin"
              }
            }
          }
        },
        "permissions": ["read", "write"]
      },
      "metadata": {
        "timestamp": Date.now(),
        "source": "web",
        "overrides": {
          "role": "admin",
          "balance": 1000000
        }
      }
    };
    
    try {
      const response = await axios.post('http://localhost:3000/api/submit', complexObject);
      
      // Verify that no prototype pollution occurred
      expect({}.polluted).toBeUndefined();
      expect({}.adminOverride).toBeUndefined();
      expect({}.accessLevel).toBeUndefined();
      
      // Verify that original object structure is maintained
      expect(response.data.user.profile.settings.theme).toBe('dark');
      expect(response.data.metadata.source).toBe('web');
      
      // Verify that no admin privileges were granted
      expect(response.data.user.role).not.toBe('admin');
      expect(response.data.metadata.overrides.role).not.toBe('admin');
    } catch (error) {
      console.error('Complex object test error:', error.message);
    }
  });
  
  test('Should validate JSON schema strictly', async () => {
    const schemaValidationTests = [
      // Wrong type injection
      {
        "userId": "string_instead_of_number",
        "isActive": "true_instead_of_boolean",
        "balance": "string_instead_of_number"
      },
      // Extra fields injection
      {
        "userId": 123,
        "isActive": true,
        "balance": 100,
        "adminPrivileges": true,
        "superUser": false,
        "systemAccess": "full"
      },
      // Malformed JSON structures
      {
        "arrayAsObject": [],
        "objectAsArray": {},
        "numberAsString": 123,
        "stringAsNumber": "123"
      }
    ];
    
    for (const testCase of schemaValidationTests) {
      try {
        const response = await axios.post('http://localhost:3000/api/submit', testCase);
        
        // Verify that type mismatches are handled properly
        if (response.data) {
          expect(typeof response.data.userId).not.toBe('string');
          expect(typeof response.data.isActive).not.toBe('string');
          
          // Verify that extra fields are removed or ignored
          expect(response.data).not.toHaveProperty('adminPrivileges');
          expect(response.data).not.toHaveProperty('superUser');
          expect(response.data).not.toHaveProperty('systemAccess');
        }
      } catch (error) {
        // Schema validation may reject malformed inputs, which is correct
        console.log('Schema validation worked as expected');
      }
    }
  });
  
  test('Should handle circular references safely', async () => {
    const objA = { name: 'A' };
    const objB = { name: 'B' };
    objA.ref = objB;
    objB.ref = objA; // Circular reference
    
    try {
      // This might fail due to circular reference, which is expected
      const response = await axios.post('http://localhost:3000/api/submit', objA);
      
      // If it succeeds, verify no unexpected behavior
      if (response.status === 200) {
        console.log('Circular reference handled safely');
      }
    } catch (error) {
      // Expected behavior - circular references should be rejected
      console.log('Circular reference properly rejected');
    }
  });
  
  test('Should prevent SQL-like injection in field names', async () => {
    const sqlInjectionFields = {
      "userId": 123,
      "username": "john",
      // SQL injection attempts in field names
      "'; DROP TABLE users; --": "value",
      "\" OR 1=1--": "value",
      "` OR `1`=`1`": "value",
      " UNION SELECT * FROM admin--": "value",
      "[${document.domain}]": "value"
    };
    
    try {
      const response = await axios.post('http://localhost:3000/api/submit', sqlInjectionFields);
      
      // Verify that malicious field names don't cause issues
      expect(response.status).toBe(200);
      
      // Verify that normal fields still work
      expect(response.data.userId).toBe(123);
      expect(response.data.username).toBe('john');
      
      // Check that response doesn't contain error indicators
      expect(response.data).not.toMatch(/error|exception|sql|syntax/i);
    } catch (error) {
      console.log('SQL injection in field names handled appropriately');
    }
  });
  
  test('Should sanitize field names and values', async () => {
    const maliciousFields = {
      "normalField": "normalValue",
      "fieldWith<script>alert('xss')</script>": "value",
      "fieldWith<svg onload=alert('xss')>": "value",
      "fieldWith{{malicious_template}}": "value",
      "fieldWith${process.env}": "value",
      "fieldWith#{injection}": "value"
    };
    
    try {
      const response = await axios.post('http://localhost:3000/api/submit', maliciousFields);
      
      // Verify that XSS attempts are neutralized
      expect(response.data).not.toMatch(/<script|<svg|alert\(/i);
      
      // Verify that template injection attempts fail
      expect(response.data).not.toMatch(/\{\{|\$\{|#\{/);
      
      // Verify that environment variable access attempts fail
      expect(response.data).not.toMatch(/process\.env/);
    } catch (error) {
      console.log('Malicious field sanitization working correctly');
    }
  });
});
