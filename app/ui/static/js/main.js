window.ratesFilterComponent = function () {
  return {
    ratesData: [],
    loading: false,
    error: null,
    searchValue: '',
    currencySelected: '',
    bankSelected: '',
    rateTypeSelected: 'tt',
    get hasActiveFilters() {
      return this.searchValue.trim() || this.currencySelected || this.bankSelected || this.rateTypeSelected;
    },
    get enrichedRatesData() {
      return this.ratesData.map(rate => ({
        ...rate,
        _computed: {
          flag: this.getCurrencyFlag(rate.currency.code),
          bgColor: this.getCurrencyBgColor(rate.currency.code)
        }
      }));
    },
    handleSearchInput() {
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
    getCurrencyFlag(currencyCode) {
      const flagMap = {
        'USD': '🇺🇸',
        'EUR': '🇪🇺',
        'GBP': '🇬🇧',
        'JPY': '🇯🇵',
        'SGD': '🇸🇬',
        'AUD': '🇦🇺',
        'CHF': '🇨🇭',
        'KWD': '🇰🇼',
        'OMR': '🇴🇲',
        'SAR': '🇸🇦',
        'AED': '🇦🇪',
        'QAR': '🇶🇦',
        'JOD': '🇯🇴',
        'BHD': '🇧🇭',
        'INR': '🇮🇳',
        'CAD': '🇨🇦',
        'NZD': '🇳🇿',
        'ZAR': '🇿🇦',
        'DKK': '🇩🇰',
        'KRW': '🇰🇷',
        'SEK': '🇸🇪',
        'NOK': '🇳🇴',
        'CNY': '🇨🇳',
        'MYR': '🇲🇾',
        'HKD': '🇭🇰',
        'THB': '🇹🇭'
      };
      return flagMap[currencyCode] || '🏴';
    },
    getCurrencyBgColor(currencyCode) {
      const bgMap = {
        'USD': 'bg-gradient-to-br from-emerald-400 via-teal-500 to-cyan-600',
        'EUR': 'bg-gradient-to-br from-indigo-400 via-blue-500 to-cyan-600',
        'GBP': 'bg-gradient-to-br from-pink-400 via-purple-500 to-indigo-600',
        'JPY': 'bg-gradient-to-br from-red-400 via-pink-500 to-yellow-400',
        'SGD': 'bg-gradient-to-br from-green-400 via-teal-500 to-blue-400',
        'AUD': 'bg-gradient-to-br from-yellow-400 via-orange-500 to-red-600',
        'CHF': 'bg-gradient-to-br from-gray-400 via-gray-500 to-gray-700',
        'KWD': 'bg-gradient-to-br from-yellow-300 via-yellow-500 to-yellow-700',
        'OMR': 'bg-gradient-to-br from-orange-300 via-orange-500 to-orange-700',
        'SAR': 'bg-gradient-to-br from-green-300 via-green-500 to-green-700',
        'AED': 'bg-gradient-to-br from-blue-300 via-blue-500 to-blue-700',
        'QAR': 'bg-gradient-to-br from-cyan-300 via-cyan-500 to-cyan-700',
        'JOD': 'bg-gradient-to-br from-red-300 via-red-500 to-red-700',
        'BHD': 'bg-gradient-to-br from-pink-300 via-pink-500 to-pink-700',
        'INR': 'bg-gradient-to-br from-orange-400 via-yellow-500 to-green-400',
        'CAD': 'bg-gradient-to-br from-red-400 via-orange-500 to-yellow-400',
        'NZD': 'bg-gradient-to-br from-green-400 via-blue-500 to-indigo-400',
        'ZAR': 'bg-gradient-to-br from-purple-400 via-violet-500 to-purple-600',
        'DKK': 'bg-gradient-to-br from-red-300 via-red-500 to-red-700',
        'KRW': 'bg-gradient-to-br from-blue-400 via-indigo-500 to-purple-600',
        'SEK': 'bg-gradient-to-br from-blue-300 via-yellow-400 to-blue-600',
        'NOK': 'bg-gradient-to-br from-red-400 via-blue-500 to-red-600',
        'CNY': 'bg-gradient-to-br from-red-400 via-yellow-500 to-red-600',
        'MYR': 'bg-gradient-to-br from-blue-400 via-red-500 to-yellow-600',
        'HKD': 'bg-gradient-to-br from-red-400 via-red-500 to-red-700',
        'THB': 'bg-gradient-to-br from-red-300 via-blue-400 to-red-600'
      };
      return bgMap[currencyCode] || 'bg-gradient-to-br from-emerald-400 via-teal-500 to-cyan-600';
    },
    formatRateType(rateName, rateType) {
      if (!rateName.includes("All")) {
        if (rateType.includes('buying')) {
          return 'Buy Rate';
        } else if (rateType.includes('selling')) {
          return 'Sell Rate';
        }
      }

      return rateType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    },
    resetAllFilters() {
      this.searchValue = '';
      this.currencySelected = '';
      this.bankSelected = '';
      this.rateTypeSelected = '';

      // Reset dropdown displays by dispatching custom reset events
      window.dispatchEvent(new CustomEvent('reset-filters'));

      this.triggerUpdate();
    }
  };
}