

    <script>
        // Connect to the WebSocket server
        const socket = new WebSocket("ws://localhost:8765");

        // Initialize D3.js chart
        const margin = {top: 20, right: 20, bottom: 30, left: 50};
        const width = 600 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        const svg = d3.select("#chart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        const x = d3.scaleLinear()
            .domain([0, 10])  // Assuming 10 data points
            .range([0, width]);

        const y = d3.scaleLinear()
            .domain([0, 100])  // Assuming temperature and humidity range from 0 to 100
            .range([height, 0]);

        const line = d3.line()
            .x((d, i) => x(i))
            .y((d) => y(d));

        const path = svg.append("path")
            .datum([])
            .attr("class", "line")
            .attr("d", line);

        // Function to update chart with new data
        function updateChart(newData) {
            // Append new data to the existing data array
            const data = path.datum();
            data.push(newData);

            // Redraw the line
            path.attr("d", line);

            // Shift the x-axis domain
            x.domain([data.length - 10, data.length]);
        }

        // Event listener for WebSocket messages
        socket.addEventListener("message", function(event) {
            // Parse JSON message
            const data = JSON.parse(event.data);

            // Update chart with new data
            updateChart(data.temperature);
        });
    </script>
</body>
</html>