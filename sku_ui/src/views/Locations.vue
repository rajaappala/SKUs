<template>
  <div class="mt-3">
    <b-alert :variant="alert.variant" :show="alert.show">{{ alert.message }}</b-alert>
    <div class="float-right pt-3 pb-3">
      <b-button type="button" variant="primary" v-b-modal.location-modal>
        Add location</b-button
      >
    </div>
    <b-table striped hover :items="locations" :fields="fields">
      <template v-slot:cell(actions)="row">
        <b-button
          @click="editLocation(row.item, row.index, $event.target)"
          class="mr-1"
          size="sm"
          variant="secondary"
        >
          Edit
        </b-button>
        <b-button variant="info" size="sm" class="mr-1" @click="row.toggleDetails">
          {{ row.detailsShowing ? "Hide" : "Show" }} Details
        </b-button>
        <b-button
          @click="deleteLocation(row.item, row.index, $event.target)"
          size="sm"
          variant="danger"
        >
          Delete
        </b-button>
      </template>

      <template v-slot:row-details="row">
        <b-card>
          <ul>
            <li v-for="(value, key) in row.item" :key="key">
              {{ key }}: {{ value }}
            </li>
          </ul>
        </b-card>
      </template>
    </b-table>
    <b-modal
      id="location-modal"
      ref="modal"
      :title="locationModal.title"
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOk"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          label="Name"
          :state="nameState"
          label-for="name-input"
          invalid-feedback="Name is required"
        >
          <b-form-input
            id="name-input"
            v-model="getLocation.name"
            :state="nameState"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="SKU Code"
          label-for="sku-code-input"
          :state="skuCodeState"
          invalid-feedback="SKU code is required"
        >
          <b-form-input
            id="sku-code-input"
            v-model="getLocation.sku_code"
            :state="skuCodeState"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="SKU Name"
          label-for="sku-name-input"
          :state="skuNameState"
          invalid-feedback="SKU Name is required"
        >
          <b-form-input
            id="sku-name-input"
            v-model="getLocation.sku_name"
            :state="skuNameState"
            required
          >
          </b-form-input>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
export default {
  name: "LocationComponent",
  data() {
    return {
      newLocation: {},
      nameState: null,
      skuCodeState: null,
      skuNameState: null,
      alert: {
        show: false,
        message: "",
        variant: "",
      },
      locationModal: {
        title: "Add Location",
      },
      fields: [
        "id",
        "name",
        "sku_name",
        "sku_code",
        "user",
        "last_modified",
        "actions",
      ],
    };
  },
  computed: {
    ...mapGetters({
      locations: "getLocations",
      getLocation: "getLocation",
    }),
  },
  created() {
    this.get_locations();
    this.set_breadcrumb("Locations");
  },
  methods: {
    ...mapMutations({
      set_breadcrumb: "set_breadcrumb",
      set_location: "set_location",
    }),
    ...mapActions({
      get_locations: "get_locations",
      create_location: "create_location",
      update_location: "update_location",
      delete_location: "delete_location",
    }),
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.nameState = this.getLocation.name ? true : false;
      this.skuNameState = this.getLocation.sku_name ? true : false;
      this.skuCodeState = this.getLocation.sku_code ? true : false;
      return valid;
    },
    resetModal() {
      this.nameState = null;
      this.skuNameState = null;
      this.skuCodeState = null;
      this.newLocation = null;
    },
    handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.handleSubmit();
    },
    handleSubmit() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      if (this.getLocation.id) {
        this.update_location(this.getLocation).then(() => {
          this.alert.message = "Location updated successfully";
          this.alert.variant = "success";
          this.alert.show = true;
          this.$bvModal.hide("location-modal");
          this.set_location({});
        });
      } else {
        this.create_location(this.getLocation).then(() => {
          this.$bvModal.hide("location-modal");
          this.set_location({});
          this.alert.message = "Location created successfully";
          this.alert.variant = "success";
          this.alert.show = true;
        });
      }
    },
    editLocation(item, index, event) {
      this.newLocation.id = item.id;
      this.newLocation.name = item.name;
      this.newLocation.sku_name = item.sku_name;
      this.newLocation.sku_code = item.sku_code;
      this.locationModal.titel = `Edit ${item.name}`;
      this.set_location(this.newLocation);
      this.$bvModal.show("location-modal");
    },
    deleteLocation(item, index, event) {
      this.$bvModal
        .msgBoxConfirm(`Please confirm that you want to delete ${item.name}.`, {
          title: "Please Confirm",
          size: "sm",
          buttonSize: "sm",
          okVariant: "danger",
          okTitle: "YES",
          cancelTitle: "NO",
          footerClass: "p-2",
          hideHeaderClose: false,
          centered: true,
        })
        .then((value) => {
          this.delete_location(item.id).then(() => {
            console.log("deleted successfully");
            this.alert.message = "Location deleted successfully";
            this.alert.variant = "success";
            this.alert.show = true;
          });
        })
        .catch((err) => {
          // An error occurred
        });
    },
  },
};
</script>