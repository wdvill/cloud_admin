<template>
  <div class="form-group">
    <label class="control-label col-xs-offset-2 col-xs-2 yzj-size-16 clear-left text-left text-info">
     地区</label>
     <div class="col-xs-3 clear-left">
      <select class="form-control select-control" id="address_state" v-model="province">
        <option v-for="option in provinces" v-bind:value="option">
          {[ option.name ]}
        </option>
      </select>
    </div>
    <div class="col-xs-3 clear-left">
      <select class="form-control select-control" id="address_city" v-model="city_id">
        <option v-for="option in cities" v-bind:value="option.address_id">
          {[ option.name ]}
        </option>
      </select>
    </div>
  </div>
</template>
<script>
import $ from 'jquery'
export default {
  created () {
    let _self = this
    console.log('created from lace', this.city_id)
    $.getJSON('/api/address', {address_id: 0, t: 'all'}, (data) => {
      _self.places = data.addresses
      _self.provinces = _self.getPlacesByParentId(1, _self.places)
      _self.setPlace(_self.city_id)
    })
  },
  data () {
    return {
      province: {},
      provinces: [],
      city: {},
      cities: [],
      places: []
    }
  },
  methods: {
    updateCity (option) {
    },
    getPlacesByParentId (id, places) {
      let results = []
      for (let i = 0; i < places.length; i++) {
        if (places[i].pid === id) {
          results.push(places[i])
        }
      }
      return results
    },
    getPlaceById (id, places) {
      for (let i = 0; i < places.length; i++) {
        if (places[i].address_id === id) {
          return places[i]
        }
      }
    },
    setPlace (value) {
      if (value) {
        this.city = this.getPlaceById(value, this.places)
        this.province = this.getPlaceById(this.city.pid, this.places)
        this.cities = this.getPlacesByParentId(this.province.address_id, this.places)
      } else {
        this.province = this.provinces[0]
        this.cities = this.getPlacesByParentId(this.province.address_id, this.places)
        this.city = this.cities[0]
      }
    }

  },
  props: ['city_id'],
  watch: {
    province (value) {
      this.cities = this.getPlacesByParentId(value.address_id, this.places)
      this.city = this.cities[0]
    },
    city_id (value) {
      this.setPlace(value)
    }
  }

}
</script>
