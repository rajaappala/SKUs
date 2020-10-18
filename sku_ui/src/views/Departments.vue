<template>
  <div class="mt-3">
    <b-alert :variant="alert.variant" :show="alert.show">{{
      alert.message
    }}</b-alert>
    <div class="float-right pt-3 pb-3">
      <b-button type="button" variant="primary" v-b-modal.department-modal>
        Add Department</b-button
      >
    </div>
    <b-table striped hover :items="departments" :fields="fields">
      <template v-slot:cell(location)="row">
        <span>{{ row.item.location }}</span>
      </template>
      <template v-slot:cell(actions)="row">
        <b-button
          @click="editDept(row.item, row.index, $event.target)"
          class="mr-1"
          size="sm"
          variant="secondary"
        >
          Edit
        </b-button>
        <b-button
          variant="info"
          size="sm"
          class="mr-1"
          @click="row.toggleDetails"
        >
          {{ row.detailsShowing ? "Hide" : "Show" }} Details
        </b-button>
        <b-button
          @click="deleteDept(row.item, row.index, $event.target)"
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
      id="department-modal"
      ref="modal"
      :title="deptModal.title"
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
            v-model="getDept.name"
            :state="nameState"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="Location"
          label-for="location-input"
          :state="locationState"
          invalid-feedback="Location is required"
        >
          <b-form-select
            id="location-input"
            v-model="getDept.location"
            :options="getLocationsFordepartment"
          ></b-form-select>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
import _ from "lodash";

export default {
  name: "DepartmentComponent",
  data() {
    return {
      newDept: {},
      nameState: null,
      locationState: null,
      alert: {
        show: false,
        message: "",
        variant: "",
      },
      deptModal: {
        title: "Add Department",
      },
      fields: ["id", "name", "location", "user", "last_modified", "actions"],
    };
  },
  computed: {
    ...mapGetters({
      departments: "getDepartments",
      getDept: "getDept",
      getLocationsFordepartment: "getLocationsFordepartment",
    }),
  },
  created() {
    this.get_departments();
    this.set_breadcrumb("Departments");
  },
  methods: {
    ...mapMutations({
      set_breadcrumb: "set_breadcrumb",
      set_department: "set_department",
    }),
    ...mapActions({
      get_departments: "get_departments",
      create_department: "create_department",
      update_department: "update_department",
      delete_department: "delete_department",
    }),
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.nameState = this.getDept.name ? true : false;
      this.locationState = this.getDept.location ? true : false;
      return valid;
    },
    resetModal() {
      this.nameState = null;
      this.locationState = null;
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
      if (this.getDept.id) {
        this.update_department(this.getDept).then(() => {
          this.alert.message = "Department updated successfully";
          this.alert.variant = "success";
          this.alert.show = true;
          this.$bvModal.hide("department-modal");
          this.set_department({});
        });
      } else {
        this.create_department(this.getDept).then(() => {
          this.$bvModal.hide("department-modal");
          this.set_department({});
          this.alert.message = "Department created successfully";
          this.alert.variant = "success";
          this.alert.show = true;
        });
      }
    },
    editDept(item, index, event) {
      this.newDept.id = item.id;
      this.newDept.name = item.name;
      debugger;
      this.newDept.location = _.find(this.getLocationsFordepartment, (val) => {
        if (val.text == item.location) return val;
      }).value;
      this.deptModal.titel = `Edit ${item.name}`;
      this.set_department(this.newDept);
      this.$bvModal.show("department-modal");
    },
    deleteDept(item, index, event) {
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
          this.delete_department(item.id).then(() => {
            this.alert.message = "Department deleted successfully";
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