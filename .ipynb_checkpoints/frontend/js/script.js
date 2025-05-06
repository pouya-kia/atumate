var btnLangE = document.querySelector('.btn-lang-item-E');
var btnLangF = document.querySelector('.btn-lang-item-F');

const clickHandlerE = event => {
    btnLangE.classList.add('lang-active');
    btnLangF.classList.remove('lang-active');
}

btnLangE.addEventListener('click', clickHandlerE);

///////////////////////

const clickHandlerF = event => {
    btnLangF.classList.add('lang-active');
    btnLangE.classList.remove('lang-active');
}

btnLangF.addEventListener('click', clickHandlerF);

///////////////////////

var btnUp = document.querySelector('.btn-item-up');
var btnIn = document.querySelector('.btn-item-in');

const hoverUpBtn = event => {
    btnIn.classList.add('mark');
}

btnUp.addEventListener('mouseover', hoverUpBtn);

const mouseoutUpBtn = event => {
    btnIn.classList.remove('mark');
}

btnUp.addEventListener('mouseout', mouseoutUpBtn);

////////////////////////////////

let uploadedDataJson = null;

document.getElementById('fileInput').addEventListener('change', function () {
  const file = this.files[0];
  const fileNameDisplay = document.getElementById('fileName');
  const progressBar = document.getElementById('progressBar');
  const progressContainer = document.querySelector('.progress-container');
  const showArrow = document.querySelector('.arrow');
  const showBtnArrow = document.querySelector('.btn-arrow');

  if (!file) return;

  fileNameDisplay.textContent = file.name;
  progressContainer.style.display = "block";
  let progress = 0;

  const interval = setInterval(() => {
    if (progress >= 100) {
      clearInterval(interval);
      showArrow.classList.remove('d-hide');
      showArrow.classList.add('d-show');
      showBtnArrow.classList.remove('d-hide');
      showBtnArrow.classList.add('d-show');
      progressContainer.classList.add('d-hide');
    } else {
      progress += 10;
      progressBar.style.width = progress + "%";
    }
  }, 500);

  // ✅ Convert CSV to JSON
  const reader = new FileReader();
  reader.onload = function (e) {
    const csv = e.target.result;
    const lines = csv.split("\n").filter(line => line.trim() !== "");
    const headers = lines[0].split(",");

    const jsonData = [];

    for (let i = 1; i < lines.length; i++) {
      const obj = {};
      const currentLine = lines[i].split(",");

      if (currentLine.length === headers.length) {
        headers.forEach((header, index) => {
          obj[header.trim()] = currentLine[index].trim();
        });
        jsonData.push(obj);
      }
    }

    uploadedDataJson = JSON.stringify(jsonData);
    console.log("✅ File converted to JSON:", uploadedDataJson);
    alert("✅ File successfully loaded and converted to JSON!");
  };

  reader.readAsText(file);
});

/////////////////////////////////////

window.addEventListener('resize', function () {
    if (window.innerWidth <= 992) {
        // document.querySelector('#About').id("About-sub");
        document.querySelector('.about').id = "About-sub";
    }
});

/////////////////////////////////////

// ✅ Submit JSON + config to API

document.getElementById("submitToAPI").addEventListener("click", function () {
  if (!uploadedDataJson) {
    alert("⛔️ Please upload a file first.");
    return;
  }

  const config = {
    drop_columns: ["id"], // این رو بر اساس داده‌ات تنظیم کن
    encoding: ["gender"], // و این هم همینطور
    model: {
      mode: "supervised",
      type: "logistic",
      target: "target",
      scaler: "standard",
      params: {
        max_iter: 500
      }
    }
  };

  fetch("http://127.0.0.1:8000/api/run-pipeline", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      data: JSON.parse(uploadedDataJson),  // دقت کن که باید parse بشه!
      config: config
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log("✅ API Response:", result);

      if (!result.data || !Array.isArray(result.data)) {
        alert("⚠️ No prediction data returned.");
        return;
      }

      // ✅ ذخیره نتایج در localStorage برای صفحه جدید
      localStorage.setItem("predictions", JSON.stringify(result.data));

      // ✅ رفتن به صفحه جدید برای نمایش نتایج
      window.open("results.html", "_blank");
    })
    .catch(error => {
      console.error("❌ Error calling API:", error);
      alert("❌ Failed to call pipeline API.");
    });
});



// document.getElementById("submitToAPI").addEventListener("click", function () {
//   if (!uploadedDataJson) {
//     alert("⛔️ Please upload a file first.");
//     return;
//   }

//   const config = {
//     drop_columns: ["id"],  // یا هر ستون اضافی که باید حذف بشه
//     encoding: ["gender"],  // یا ستون‌هایی که برای encoding لازم داری
//     model: {
//       mode: "supervised",
//       type: "logistic",
//       target: "target",
//       scaler: "standard",
//       params: {
//         max_iter: 500
//       }
//     }
//   };

//   // 👇 اینجا قرارش بده:
//   fetch("http://127.0.0.1:8000/api/run-pipeline", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json"
//     },
//     body: JSON.stringify({
//       data: JSON.parse(uploadedDataJson),  // ⚠️ دقت کن که string نیست!
//       config: config
//     })
//   })
//   .then(response => response.json())
//   .then(result => {
//     console.log("✅ API Response:", result);
//     alert("✅ Pipeline executed! Check console for details.");

//     const resultsContainer = document.getElementById("resultsContainer");
//     const resultsTableBody = document.querySelector("#resultsTable tbody");

//     resultsTableBody.innerHTML = "";

//     if (result.data && Array.isArray(result.data) && result.data.length > 0) {
//       const headers = Object.keys(result.data[0]); // گرفتن عنوان ستون‌ها
  
//       // نمایش عنوان ستون‌ها در thead
//       const thead = document.querySelector("#resultsTable thead");
//       thead.innerHTML = "<tr><th>#</th>" + headers.map(h => `<th>${h}</th>`).join("") + "</tr>";
  
//       // نمایش فقط ۵ ردیف اول
//       result.data.slice(0, 5).forEach((row, index) => {
//         const tr = document.createElement("tr");
//         tr.innerHTML = `<td>${index + 1}</td>` + headers.map(h => `<td>${row[h]}</td>`).join("");
//         resultsTableBody.appendChild(tr);
//       });
  
//       resultsContainer.style.display = "block";
//     }
//   })
//   .catch(error => {
//     console.error("❌ Error calling API:", error);
//     alert("❌ Failed to call pipeline API.");
//   });
// });







// document.getElementById("submitToAPI").addEventListener("click", function () {
//   if (!uploadedDataJson) {
//     alert("⛔️ Please upload a file first.");
//     return;
//   }

//   const config = {
//     drop_columns: ["id"],
//     encoding: ["gender"],
//     model: {
//       mode: "supervised",
//       type: "logistic",
//       target: "target",
//       scaler: "standard",
//       params: {
//         max_iter: 500
//       }
//     }
//   };

//   fetch("http://127.0.0.1:8000/api/run-pipeline", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json"
//     },
//     body: JSON.stringify({
//       data: JSON.parse(uploadedDataJson),
//       config: config
//     })
//   })
//     .then(response => response.json())
//     .then(result => {
//       console.log("✅ API Response:", result);
//       alert("✅ Pipeline executed! Check console for details.");

//       const resultsContainer = document.getElementById("resultsContainer");
//       const resultsTableBody = document.querySelector("#resultsTable tbody");

//       resultsTableBody.innerHTML = ""; // پاک‌سازی قبلی

//       if (result.data && Array.isArray(result.data) && result.data.length > 0) {
//         const headers = Object.keys(result.data[0]); // گرفتن عنوان ستون‌ها
    
//         // نمایش عنوان ستون‌ها در thead
//         const thead = document.querySelector("#resultsTable thead");
//         thead.innerHTML = "<tr><th>#</th>" + headers.map(h => `<th>${h}</th>`).join("") + "</tr>";
    
//         // نمایش فقط ۵ ردیف اول
//         result.data.slice(0, 5).forEach((row, index) => {
//           const tr = document.createElement("tr");
//           tr.innerHTML = `<td>${index + 1}</td>` + headers.map(h => `<td>${row[h]}</td>`).join("");
//           resultsTableBody.appendChild(tr);
//         });
    
//       // if (result.data && Array.isArray(result.data)) {
//       //   result.data.forEach((row, index) => {
//       //     const tr = document.createElement("tr");
//       //     const tdIndex = document.createElement("td");
//       //     const tdPred = document.createElement("td");
//       //     const tdProb = document.createElement("td");

//       //     tdIndex.textContent = index + 1;
//       //     tdPred.textContent = row.prediction ?? "—";
//       //     tdProb.textContent = row.probability ?? "—";

//       //     tr.appendChild(tdIndex);
//       //     tr.appendChild(tdPred);
//       //     tr.appendChild(tdProb);
//       //     resultsTableBody.appendChild(tr);
//       //   });

//         resultsContainer.style.display = "block";
//       }
//     })
//     .catch(error => {
//       console.error("❌ Error calling API:", error);
//       alert("❌ Failed to call pipeline API.");
//     });
// });
