<template>
    <v-row justify="center">
      <v-dialog v-model="dialog" persistent max-width="900px">
        <!-- <template v-slot:activator="{ on, attrs }">
          <v-btn color="primary" dark v-bind="attrs" v-on="on">Open Dialog</v-btn>
        </template>-->
        
        <v-card>
          <v-card-title>
            <span class="headline primary--text">{{
              __('Create POS Opening Shift')
            }}</span>
          </v-card-title>
          <v-card-text>
            <v-container >
              <v-row>
                <v-col cols="6">
                  <v-autocomplete
                    :items="companys"
                    :label="frappe._('Company')"
                    v-model="company"
                    required
                  ></v-autocomplete>
                </v-col>
                <v-col cols="6">
                  <v-autocomplete
                    :items="pos_profiles"
                    :label="frappe._('POS Profile')"
                    v-model="pos_profile"
                    required
                  ></v-autocomplete>
                </v-col>
     
                <v-col cols="6">
                  <template>
                    <v-data-table
                      :headers="payments_methods_headers"
                      :items="payments_methods"
                      item-key="mode_of_payment"
                      class="elevation-1"
                      :items-per-page="itemsPerPage"
                      hide-default-footer
                    >
                      <template v-slot:item.amount="props">
                        <v-edit-dialog :return-value.sync="props.item.amount">
                          {{ formtCurrency(props.item.amount) }}
                          <template v-slot:input>
                            <v-text-field
                              v-model="props.item.amount"
                              :rules="[max25chars]"
                              :label="frappe._('Edit')"
                              single-line
                              counter
                              type="number"
                            ></v-text-field>
                          </template>
                        </v-edit-dialog>
                      </template>
                    </v-data-table>
                  </template>
                </v-col>
                <v-col cols="6">
                  <template>
                    <!-- <v-data-table
                      :headers="denomination_headers"
                      :items="denomination_data"
                      item-key="currency"
                      class="elevation-1"
                      :items-per-page="itemsPerPage"
                      hide-default-footer
                      v-model="table"
                    >
                      <template v-slot:item.amount="props">
                        <v-edit-dialog :return-value.sync="props.item.amount">
                          {{ formtCurrency(props.item.amount) }}
                          <template v-slot:input>
                            <v-text-field
                              v-model="props.item.amount"
                              :rules="[max25chars]"
                              :label="frappe._('Edit')"
                              single-line
                              counter
                              type="number"
                            ></v-text-field>
                          </template>
                        </v-edit-dialog>
                      </template>
                      <template v-slot:item.count="props">
                      <v-edit-dialog :return-value.sync="props.item.count">
                        {{ props.item.count }}
                        <template v-slot:input>
                          <v-text-field
                            v-model="props.item.count"
                            :rules="[max25chars]"
                            :label="frappe._('Edit')"
                            single-line
                            counter
                            type="number"
                            @change="update_amount($event,props.item)"
                          ></v-text-field>
                        </template>
                      </v-edit-dialog>
                    </template>
                    </v-data-table> -->
                    <v-simple-table>
                        <template v-slot:default>
                          <thead>
                            <tr>
                              <th class="text-center" width='100px'>
                                Currency
                              </th>
                              <th class="text-center" width='100px'>
                                Count
                              </th>
                              <th class="text-center" width='100px'>
                                Amount
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr
                            v-for="items in denomination_data"
                            :key="items.currency">
                              <td><v-text-field placeholder="Currency" v-model="items.currency" dense readonly></v-text-field></td>
                              <td><v-text-field placeholder="Count" v-model="items.count" dense @change="update_amount($event,items)"></v-text-field></td>
                              <td><v-text-field placeholder="Amount" v-model="items.amount" dense readonly></v-text-field></td>
                            </tr>
                          </tbody>
                        </template>
                      </v-simple-table>
                  </template>
                </v-col>
  
  
  
              </v-row>
              
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" dark @click="go_desk">Cancel</v-btn>
            <v-btn color="success" dark @click="submit_dialog">Submit</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </template>
  
  <script>
  import { evntBus } from '../../bus';
  export default {
    props: ['dialog'],
    data: () => ({
      dialog_data: {},
      companys: [],
      company: '',
      pos_profiles_data: [],
      pos_profiles: [],
      pos_profile: '',
      payments_method_data: [],
      payments_methods: [],
      currency : [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1],
      table:[],
      payments_methods_headers: [
        {
          text: __('Mode of Payment'),
          align: 'start',
          sortable: false,
          value: 'mode_of_payment',
        },
        {
          text: __('Opening Amount'),
          value: 'amount',
          align: 'center',
          sortable: false,
        },
        ],
        denomination_headers:[
        {
          text: __('Currency'),
          align: 'start',
          sortable: false,
          value: 'currency',
        },
        {
          text: __('Count'),
          value: 'count',
          align: 'center',
          sortable: false,
          
        },
        {
          text: __('Amount'),
          value: 'amount',
          align: 'center',
          sortable: false,
        },
        ],
        denomination_data:[],
      itemsPerPage: 100,
      max25chars: (v) => v.length <= 12 || 'Input too long!', // TODO : should validate as number
      pagination: {},
      snack: false, // TODO : need to remove
      snackColor: '', // TODO : need to remove
      snackText: '', // TODO : need to remove
    }),
    watch: {
      company(val) {
        this.pos_profiles = [];
        this.pos_profiles_data.forEach((element) => {
          if (element.company === val) {
            this.pos_profiles.push(element.name);
          }
          if (this.pos_profiles.length) {
            this.pos_profile = this.pos_profiles[0];
          } else {
            this.pos_profile = '';
          }
        });
      },
      pos_profile(val) {
        this.payments_methods = [];
        this.payments_method_data.forEach((element) => {
          if (element.parent === val) {
            this.payments_methods.push({
              mode_of_payment: element.mode_of_payment,
              amount: 0,
              is_cash:element.is_cash
            });
          }
        });
      },
    },
    methods: {
      update_amount(value,row){
        row.amount = row.currency * row.count
        let total_amount = 0
        this.denomination_data.forEach((data) =>{
          total_amount += data.amount
        })
        this.payments_methods.forEach((m)=>{
          if (m.is_cash){
            m.amount = total_amount
          }
        })
      },
      close_opening_dialog() {
        evntBus.$emit('close_opening_dialog');
      },
      get_opening_dialog_data() {
        const vm = this;
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.get_opening_dialog_data',
          args: {},
          callback: function (r) {
            if (r.message) {
              r.message.companys.forEach((element) => {
                vm.companys.push(element.name);
              });
              vm.company = vm.companys[0];
              vm.pos_profiles_data = r.message.pos_profiles_data;
              vm.payments_method_data = r.message.payments_method;
            }
          },
        });
      },
      submit_dialog() {
        if (!this.payments_methods.length || !this.company || !this.pos_profile) {
          return;
        }
        const vm = this;
        return frappe
          .call('posawesome.posawesome.api.posapp.create_opening_voucher', {
            pos_profile: this.pos_profile,
            company: this.company,
            balance_details: this.payments_methods,
            denomination_data:this.denomination_data
          })
          .then((r) => {
            if (r.message) {
              evntBus.$emit('register_pos_data', r.message);
              evntBus.$emit('set_company', r.message.company);
              vm.close_opening_dialog();
            }
          });
      },
      formtCurrency(value) {
        value = parseFloat(value);
        return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
      },
      go_desk() {
        frappe.set_route('/');
        location.reload();
      },
    },
  
    created: function () {
      this.$nextTick(function () {
        this.get_opening_dialog_data();
      });
      this.currency.forEach((i) => {
      this.denomination_data.push(   {
          "currency":i,
          "count":0,
          "amount":0
        },)
      })
    },
  };
  
  </script>
  