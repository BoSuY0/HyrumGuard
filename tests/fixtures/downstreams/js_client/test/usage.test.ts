import { parseResult, Client } from "demo-lib";

const internals = require("demo-lib/lib/_secret");

test("error message contract", () => {
  expect(() => parseResult({})).toThrow(/missing token/);
});

test("json shape contract", () => {
  const payload = new Client().toJSON();
  expect(payload).toHaveProperty("status");
  expect(payload.items).toEqual([]);
});

test("private symbol contract", () => {
  expect(internals.normalizePayload({ status: "ok" }).status).toBe("ok");
});
