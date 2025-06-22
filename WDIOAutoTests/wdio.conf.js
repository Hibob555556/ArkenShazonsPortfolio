export const config = {
  // ====================
  // Runner Configuration
  // ====================

  runner: "local",

  // ==================
  // Specify Test Files
  // ==================
  specs: ["./Tests/Specs/*.test.js"],
  // Patterns to exclude.
  exclude: [],

  // ============
  // Capabilities
  // ============
  maxInstances: 10,
  capabilities: [
    {
      browserName: "chrome",
    },
  ],

  // ===================
  // Test Configurations
  // ===================
  logLevel: "warn",
  bail: 0,
  // Default timeout for all waitFor* commands.
  waitforTimeout: 10000,
  // if browser driver or grid doesn't send response
  connectionRetryTimeout: 120000,
  // Default request retries count
  connectionRetryCount: 3,
  services: ["lighthouse"],
  framework: "mocha",
  reporters: ["spec"],
  mochaOpts: {
    ui: "bdd",
    timeout: 60000,
  },
};
