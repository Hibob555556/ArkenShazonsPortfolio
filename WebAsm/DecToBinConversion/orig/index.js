// Decimal To Binary Input/Output elements
const DEC_INPUT = document.getElementById("positive-num-input");
const BIN_OUTPUT = document.getElementById("binary-num");

// Binary to Decimal Input/Output elements
const BIN_INPUT = document.getElementById("binary-input");
const DEC_OUTPUT = document.getElementById("decimal-num");

Module.onRuntimeInitialized = () => {
  const DecToBin = Module.cwrap("DecToBin", "string", ["number"]);
  const BinToDec = Module.cwrap("BinToDec", "number", ["string"]);

  DEC_INPUT.addEventListener("keyup", () => {
    if (DEC_INPUT.value <= 2147483647) {
      let bin = DecToBin(`${DEC_INPUT.value}`);
      BIN_OUTPUT.textContent = bin;
    } else {
      BIN_OUTPUT.textContent = "Specified Number Is Too Large";
    }
  });

  BIN_INPUT.addEventListener("keyup", () => {
    const binStr = BIN_INPUT.value.replace(/\s+/g, ""); // remove spaces

    // Maximum binary digits for signed 32-bit int is 31
    if (binStr.length > 31) {
      DEC_OUTPUT.textContent = "Specified Number Is Too Large";
      return;
    }

    // Optional: check that string contains only 0 and 1
    if (!/^[01]*$/.test(binStr)) {
      DEC_OUTPUT.textContent = "Invalid binary number";
      return;
    }

    const dec = BinToDec(binStr);
    DEC_OUTPUT.textContent = dec;
  });
};
