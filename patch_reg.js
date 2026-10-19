const fs = require('fs');
let c = fs.readFileSync('index.html', 'utf8');

c = c.replace(/async function handleSocietyRegisterSubmit[\s\S]*?async function handleMerchantRegisterSubmit/, 
`async function handleSocietyRegisterSubmit(e) {
  if (e) e.preventDefault();
  const sName = document.getElementById("regSocietyName")?.value || "Gokuldham Co-op Housing Society";
  const secName = document.getElementById("regSecName")?.value || "Dilip Joshi";
  const secEmail = document.getElementById("regSecEmail")?.value || "secretary@gokuldham.in";
  currentUser = { id: 2, name: secName, role: "Secretary", flat: "RWA Secretariat", society: sName, email: secEmail };
  updateAuthUI();
  showAppToast("Society Registered Successfully!", "domain_add");
  navigate("secretary");
}

async function handleMerchantRegisterSubmit`);

c = c.replace(/async function handleMerchantRegisterSubmit[\s\S]*?\/\/ =========================================================================\s*\/\/ DYNAMIC WORK ITEMS BREAKDOWN HELPERS/, 
`async function handleMerchantRegisterSubmit(e) {
  if (e) e.preventDefault();
  const mName = document.getElementById("mRegName")?.value || "Ashish Sharma";
  const mAgency = document.getElementById("mRegAgency")?.value || "AquaPure Tech Services";
  const mEmail = document.getElementById("mRegEmail")?.value || "partner@aquapure.in";
  currentUser = { id: 3, name: mName, role: "Merchant", flat: "Worker Hub", society: mAgency, email: mEmail };
  updateAuthUI();
  showAppToast("Contractor Onboarded and Activated!", "construction");
  navigate("merchant");
}

// =========================================================================
// DYNAMIC WORK ITEMS BREAKDOWN HELPERS`);

fs.writeFileSync('index.html', c);
console.log('REGISTRATION INSTANT FIXED!');
