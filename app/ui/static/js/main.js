window.ratesFilterComponent = function () {
  return {
    ratesData: [],
    loading: false,
    error: null,
    searchValue: '',
    currencySelected: '',
    bankSelected: '',
    rateTypeSelected: '',
    get hasActiveFilters() {
      return this.searchValue.trim() || this.currencySelected || this.bankSelected || this.rateTypeSelected;
    },
    handleSearchInput(e) {
      this.searchValue = e.target.value.trim();

      // Only search if 2+ characters or empty (to show all)
      if (this.searchValue.length >= 2 || this.searchValue.length === 0) {
        this.triggerUpdate();
      }
    },
    async triggerUpdate() {
      this.loading = true;
      this.error = null;

      try {
        const params = new URLSearchParams();
        if (this.searchValue.trim()) params.append('search', this.searchValue.trim());
        if (this.currencySelected) params.append('currency', this.currencySelected);
        if (this.bankSelected) params.append('bank', this.bankSelected);
        if (this.rateTypeSelected) params.append('rate_type', this.rateTypeSelected);
        const queryString = params.size > 0 ? `?${params}` : '';

        const response = await fetch(`/dashboard/rates/today${queryString}`, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const jsonData = await response.json();
        this.ratesData = jsonData;

      } catch (error) {
        this.error = error.message;
        this.ratesData = [];
      } finally {
        this.loading = false;
      }
    },
    resetAllFilters() {
      this.searchValue = '';
      this.currencySelected = '';
      this.bankSelected = '';
      this.rateTypeSelected = '';

      // Clear the search input field
      document.getElementById('search-input').value = '';

      // Reset dropdown displays by dispatching custom reset events
      window.dispatchEvent(new CustomEvent('reset-filters'));

      this.triggerUpdate();
    }
  };
}