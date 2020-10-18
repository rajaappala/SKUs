<template>
  <div class="wrapper">
    <b-container class="bv-example-row">
      <form ref="form" @submit.stop.prevent="fetchGraph">
        <b-form-group
          label="Location"
          label-for="location-input"
          :state="locationState"
          invalid-feedback="Location is required"
        >
          <b-form-select
            id="location-input"
            v-model="selectedLocation"
            :options="locations"
          ></b-form-select>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
      </form>
      <div id="info-chart" ref="info-graph"></div>
    </b-container>
  </div>
</template>
<script>
import { mapGetters, mapActions } from "vuex";
import * as d3 from "d3";

export default {
  name: "InfoGraphComponent",
  data() {
    return {
      selectedLocation: null,
      locationState: null,
      locations: [],
    };
  },
  computed: {
    ...mapGetters({
      infoGraphData: "getInfoGraphData",
    }),
  },
  created() {
    this.get_locations().then((resp) => {
      this.locations = resp.data;
    });
  },
  methods: {
    ...mapActions({
      get_infograph: "get_infograph",
      get_locations: "get_locations_for_infograph",
    }),

    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.locationState = valid;
      return valid;
    },
    fetchGraph() {
      if (!this.checkFormValidity()) {
        return;
      }
      this.get_infograph(this.selectedLocation).then(() => {
        this.$refs["info-graph"].innerHTML = "";
        this.generateTree();
      });
    },
    generateTree() {
      var dx = 30;
      var dy = 200;
      let margin = { top: 10, right: 120, bottom: 10, left: 40 };
      let width = 960 - margin.right - margin.left;
      let height = 500 - margin.top - margin.bottom;

      var diagonal = d3
        .linkHorizontal()
        .x((d) => d.y)
        .y((d) => d.x);
      var tree = d3.tree().nodeSize([dx, dy]);
      const root = d3.hierarchy(this.infoGraphData);

      root.x0 = dy / 2;
      root.y0 = 0;
      root.descendants().forEach((d, i) => {
        d.id = i;
        d._children = d.children;
        if (d.depth && d.data.name.length !== 7) d.children = null;
      });

      var svg = d3
        .select("#info-chart")
        .append("svg")
        .attr("width", width + margin.right + margin.left)
        .attr("height", height + margin.top + margin.bottom)
        .attr("viewBox", [-margin.left, -margin.top, width, dx])
        .style("font", "12px sans-serif")
        .style("user-select", "none");
      const gLink = svg
        .append("g")
        .attr("fill", "none")
        .attr("stroke", "#555")
        .attr("stroke-opacity", 0.4)
        .attr("stroke-width", 1.5);

      const gNode = svg
        .append("g")
        .attr("cursor", "pointer")
        .attr("pointer-events", "all");

      function update(source) {
        const duration = d3.event && d3.event.altKey ? 2500 : 250;
        const nodes = root.descendants().reverse();
        const links = root.links();

        // Compute the new tree layout.
        tree(root);

        let left = root;
        let right = root;
        root.eachBefore((node) => {
          if (node.x < left.x) left = node;
          if (node.x > right.x) right = node;
        });

        const height = right.x - left.x + margin.top + margin.bottom;

        const transition = svg
          .transition()
          .duration(duration)
          .attr("viewBox", [-margin.left, left.x - margin.top, width, height])
          .tween(
            "resize",
            window.ResizeObserver ? null : () => () => svg.dispatch("toggle")
          );

        // Update the nodes…
        const node = gNode.selectAll("g").data(nodes, (d) => d.id);

        // Enter any new nodes at the parent's previous position.
        const nodeEnter = node
          .enter()
          .append("g")
          .attr("transform", (d) => `translate(${source.y0},${source.x0})`)
          .attr("fill-opacity", 0)
          .attr("stroke-opacity", 0)
          .on("click", (event, d) => {
            d.children = d.children ? null : d._children;
            update(d);
          });

        nodeEnter
          .append("circle")
          .attr("r", 2.5)
          .attr("fill", (d) => (d._children ? "#555" : "#999"))
          .attr("stroke-width", 10);

        nodeEnter
          .append("text")
          .attr("dy", "0.31em")
          .attr("x", (d) => (d._children ? -6 : 6))
          .attr("text-anchor", (d) => (d._children ? "end" : "start"))
          .text((d) => d.data.name)
          .clone(true)
          .lower()
          .attr("stroke-linejoin", "round")
          .attr("stroke-width", 3)
          .attr("stroke", "white");

        // Transition nodes to their new position.
        const nodeUpdate = node
          .merge(nodeEnter)
          .transition(transition)
          .attr("transform", (d) => `translate(${d.y},${d.x})`)
          .attr("fill-opacity", 1)
          .attr("stroke-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        const nodeExit = node
          .exit()
          .transition(transition)
          .remove()
          .attr("transform", (d) => `translate(${source.y},${source.x})`)
          .attr("fill-opacity", 0)
          .attr("stroke-opacity", 0);

        // Update the links…
        const link = gLink.selectAll("path").data(links, (d) => d.target.id);

        // Enter any new links at the parent's previous position.
        const linkEnter = link
          .enter()
          .append("path")
          .attr("d", (d) => {
            const o = { x: source.x0, y: source.y0 };
            return diagonal({ source: o, target: o });
          });

        // Transition links to their new position.
        link.merge(linkEnter).transition(transition).attr("d", diagonal);

        // Transition exiting nodes to the parent's new position.
        link
          .exit()
          .transition(transition)
          .remove()
          .attr("d", (d) => {
            const o = { x: source.x, y: source.y };
            return diagonal({ source: o, target: o });
          });

        // Stash the old positions for transition.
        root.eachBefore((d) => {
          d.x0 = d.x;
          d.y0 = d.y;
        });
      }

      update(root);
    },
  },
};
</script>
<style lang="scss">
.node circle {
  fill: #fff;
  stroke: steelblue;
  stroke-width: 3px;
}

.node text {
  font: 16px sans-serif;
}

.link {
  fill: none;
  stroke: #ccc;
  stroke-width: 2px;
}
</style>