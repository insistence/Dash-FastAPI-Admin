// 在独立js脚本中定义比较长的回调函数
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside_command_stats: {
        render_command_stats_chart: function (data) {

            // 根据id初始化绑定图表
            var commandStatsChart = echarts.init(document.getElementById('command-stats-charts-container'), "macarons");

            const commandStatsOption = {
              tooltip: {
                trigger: "item",
                formatter: "{a} <br/>{b} : {c} ({d}%)",
              },
              series: [
                {
                  name: "命令",
                  type: "pie",
                  roseType: "radius",
                  radius: [35, 115],
                  center: ["50%", "50%"],
                  data: data['command_stats'],
                  animationEasing: "cubicInOut",
                  animationDuration: 1000,
                }
              ]
            };

            // 渲染
            commandStatsChart.setOption(commandStatsOption);
            window.addEventListener("resize", () => {
                commandStatsChart.resize();
            });
        }
    }
});


window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside_memory: {
        render_memory_chart: function (data) {

            // 根据id初始化绑定图表
            var memoryChart = echarts.init(document.getElementById('memory-charts-container'), "macarons");

            const memoryOption = {
              tooltip: {
                formatter: "{b} <br/>{a} : " + data['used_memory_human'],
              },
              series: [
                {
                  name: "峰值",
                  type: "gauge",
                  min: 0,
                  max: 1000,
                  detail: {
                    formatter: data['used_memory_human'],
                  },
                  data: [
                    {
                      value: parseFloat(data['used_memory_human']),
                      name: "内存消耗",
                    }
                  ]
                }
              ]
            };

            // 渲染
            memoryChart.setOption(memoryOption);
            window.addEventListener("resize", () => {
                memoryChart.resize();
            });
        }
    }
});