let data = [0];

// let data = [12, 19, 3, 5, 2, 3, 12, 9, 3, 15];
let labels = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "];

// Função um Gerador de Array - dados do event.data.porc
const RepeatArrayGenerator = (datas = [], num = 1, debug = false) => {
  let result = ``;
  // do something...
  let str = `${datas.toString()},`;
  str = str.repeat(num);
  str = str.slice(0, str.length - 1);
  result = str.split(`,`);
  result = result.map((item) => {
    let newItem = "";
    newItem = item.trim() !== "" ? parseFloat(item) : "";
    return newItem;
  });
  if (debug) {
    console.log(`result =\n`, result);
  }
  return result;
};


// data = RepeatArrayGenerator(data, 6);

labels = RepeatArrayGenerator(labels, 1);

console.log(`labels =`, labels);

// data = data.concat(data);
// labels = labels.concat(labels);
// let data = [12, 19, 3, 5, 2, 3, 12, 9, 3, 15];
// let labels = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "];
var ctx = document.getElementById("myChart").getContext("2d");
// Global point options
Chart.defaults.global.elements.point.pointStyle = "circle";
// Chart.defaults.global.elements.point.pointStyle = "line";
Chart.defaults.global.elements.point.radius = 0;
var myChart = new Chart(ctx, {
  // type: "bar ",
  type: "line",
  data: {
    labels: labels,
    datasets: [
      {
        label: "CPU INFO",
        data: data,
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)",
        ],
        borderColor: [
          "rgba(255,99,132,1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],
        borderWidth: 1,
        fill: "start",
      },
    ],
  },
  options: {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
    elements: {
      line: {
        tension: 0,
        // no smooth
      },
    },
  },
});
// update
let datas = [12, 19, 3, 5, 2, 3, 12, 9, 3, 15, 12, 19, 3, 5, 2, 3, 12, 9, 3, 15];
//datas = RepeatArrayGenerator(datas, 20);

let meu_array = data;
let rodovia = new EventSource("http://localhost:8000/stream-cpu-info");
rodovia.addEventListener("msg_renan", function (event) {
  const obj = JSON.parse(event.data)
  console.log(`Adicionando ${obj.porcentagem} ao gráfico`)
  meu_array.push(obj.porcentagem)
  console.log(meu_array)
  if (meu_array.length > 20){
    meu_array.shift();
  }
  
  myChart.data.datasets[0].data = meu_array;
  myChart.update(0);  
});


// for (let i = 0; i < datas.length; i++) {
//   setTimeout(() => {
//     if (data.length > 9) {
//       data.push(datas[i]);
//       // console.log(`data =\n`, data);
//       let newData = datas[i],
//         oldData = [];
//       oldData = data.slice(data.length - 9, data.length);
//       oldData.push(newData);
//       data = oldData;
//       // console.log(`oldData =`, oldData);
//       myChart.data.datasets[0].data = data;
//       myChart.update(0);
//     } else {
//       data.push(datas[i]);
//       myChart.data.datasets[0].data = data;
//       myChart.update(0);
//     }
//   }, i * 1000);
// }

