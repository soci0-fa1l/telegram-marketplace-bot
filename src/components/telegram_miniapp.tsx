import React, { useState, useEffect } from 'react';
import { Search, Plus, Filter, Heart, ShoppingCart, User, Home, Tag, Camera, Send } from 'lucide-react';
import WalletConnect from './WalletConnect';

interface Product {
  id: number;
  title: string;
  price: number;
  category: string;
  image: string;
  seller: string;
  location: string;
  likes: number;
  isNew: boolean;
}

const TelegramMarketplace = () => {
  const [activeTab, setActiveTab] = useState('home');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [products, setProducts] = useState<Product[]>([]);
  const [showAddProduct, setShowAddProduct] = useState(false);

  // 샘플 데이터
  const categories = [
    { id: 'all', name: '전체', icon: '🏪' },
    { id: 'electronics', name: '전자기기', icon: '📱' },
    { id: 'fashion', name: '패션', icon: '👕' },
    { id: 'books', name: '도서', icon: '📚' },
    { id: 'sports', name: '스포츠', icon: '⚽' },
    { id: 'beauty', name: '뷰티', icon: '💄' }
  ];

  const sampleProducts = [
    {
      id: 1,
      title: 'iPhone 15 Pro',
      price: 1200000,
      category: 'electronics',
      image: '📱',
      seller: 'TechUser',
      location: '서울 강남구',
      likes: 12,
      isNew: true
    },
    {
      id: 2,
      title: '나이키 에어맥스',
      price: 150000,
      category: 'fashion',
      image: '👟',
      seller: 'FashionLover',
      location: '부산 해운대구',
      likes: 8,
      isNew: false
    },
    {
      id: 3,
      title: '클린 코드 도서',
      price: 25000,
      category: 'books',
      image: '📖',
      seller: 'BookWorm',
      location: '인천 연수구',
      likes: 5,
      isNew: true
    }
  ];

  useEffect(() => {
    setProducts(sampleProducts);
  }, []);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ko-KR').format(price) + '원';
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // 홈 화면
  const HomeScreen = () => (
    <div className="pb-20">
      {/* 검색 바 */}
      <div className="sticky top-0 bg-white z-10 p-4 border-b">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="상품을 검색해보세요..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-gray-100 rounded-xl border-none outline-none"
          />
        </div>
      </div>

      {/* 카테고리 */}
      <div className="p-4">
        <div className="flex gap-2 overflow-x-auto pb-2">
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`flex flex-col items-center min-w-16 p-3 rounded-xl transition-all ${
                selectedCategory === category.id 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-100 text-gray-700'
              }`}
            >
              <span className="text-2xl mb-1">{category.icon}</span>
              <span className="text-xs font-medium">{category.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* 상품 목록 */}
      <div className="px-4">
        <div className="grid grid-cols-2 gap-4">
          {filteredProducts.map(product => (
            <div key={product.id} className="bg-white rounded-xl shadow-sm border overflow-hidden">
              <div className="aspect-square bg-gray-100 flex items-center justify-center text-6xl">
                {product.image}
              </div>
              <div className="p-3">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-medium text-sm line-clamp-2 flex-1">{product.title}</h3>
                </div>
                <p className="text-lg font-bold text-blue-600 mb-1">{formatPrice(product.price)}</p>
                <p className="text-xs text-gray-500 mb-1">{product.location}</p>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-600">❤️ {product.likes}</span>
                  {product.isNew && (
                    <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full">NEW</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // 상품 등록 화면
  const AddProductScreen = () => {
    const [productForm, setProductForm] = useState<{ title: string; price: string; category: string; description: string; location: string }>({
      title: '',
      price: '',
      category: 'electronics',
      description: '',
      location: ''
    });

    return (
      <div className="p-4 pb-20">
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <h2 className="text-xl font-bold mb-6">상품 등록</h2>
          
          {/* 이미지 추가 */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">상품 이미지</label>
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center">
              <Camera className="w-12 h-12 mx-auto text-gray-400 mb-2" />
              <p className="text-gray-500 text-sm">이미지를 추가해주세요</p>
              <button className="mt-2 bg-blue-500 text-white px-4 py-2 rounded-lg text-sm">
                이미지 선택
              </button>
            </div>
          </div>

          {/* 상품명 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">상품명</label>
            <input
              type="text"
              value={productForm.title}
              onChange={(e) => setProductForm({...productForm, title: e.target.value})}
              placeholder="상품명을 입력하세요"
              className="w-full p-3 border border-gray-300 rounded-xl outline-none focus:border-blue-500"
            />
          </div>

          {/* 가격 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">가격</label>
            <input
              type="number"
              value={productForm.price}
              onChange={(e) => setProductForm({...productForm, price: e.target.value})}
              placeholder="가격을 입력하세요"
              className="w-full p-3 border border-gray-300 rounded-xl outline-none focus:border-blue-500"
            />
          </div>

          {/* 카테고리 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">카테고리</label>
            <select
              value={productForm.category}
              onChange={(e) => setProductForm({...productForm, category: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-xl outline-none focus:border-blue-500"
            >
              {categories.slice(1).map(category => (
                <option key={category.id} value={category.id}>
                  {category.icon} {category.name}
                </option>
              ))}
            </select>
          </div>

          {/* 설명 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">상품 설명</label>
            <textarea
              value={productForm.description}
              onChange={(e) => setProductForm({...productForm, description: e.target.value})}
              placeholder="상품에 대한 자세한 설명을 입력하세요"
              rows={4}
              className="w-full p-3 border border-gray-300 rounded-xl outline-none focus:border-blue-500 resize-none"
            />
          </div>

          {/* 위치 */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">거래 위치</label>
            <input
              type="text"
              value={productForm.location}
              onChange={(e) => setProductForm({...productForm, location: e.target.value})}
              placeholder="거래 희망 지역을 입력하세요"
              className="w-full p-3 border border-gray-300 rounded-xl outline-none focus:border-blue-500"
            />
          </div>

          {/* 등록 버튼 */}
          <button className="w-full bg-blue-500 text-white py-4 rounded-xl font-medium text-lg flex items-center justify-center gap-2 hover:bg-blue-600 transition-colors">
            <Send className="w-5 h-5" />
            상품 등록하기
          </button>
        </div>
      </div>
    );
  };

  // 프로필 화면
  const ProfileScreen = () => (
    <div className="p-4 pb-20">
      <div className="bg-white rounded-xl p-6 shadow-sm mb-4">
        <div className="text-center mb-6">
          <div className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-3">
            U
          </div>
          <h2 className="text-xl font-bold">사용자 이름</h2>
          <p className="text-gray-500">@username</p>
        </div>
        
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-2xl font-bold text-blue-500">12</p>
            <p className="text-sm text-gray-600">판매중</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-green-500">8</p>
            <p className="text-sm text-gray-600">판매완료</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-purple-500">5</p>
            <p className="text-sm text-gray-600">찜한상품</p>
          </div>
        </div>
      </div>

      <div className="space-y-2">
        {[
          { icon: '🛒', title: '내 상품 관리', desc: '등록한 상품을 관리하세요' },
          { icon: '💝', title: '찜한 상품', desc: '관심있는 상품을 확인하세요' },
          { icon: '💰', title: '거래 내역', desc: '구매/판매 내역을 확인하세요' },
          { icon: '⚙️', title: '설정', desc: '알림 및 계정 설정' }
        ].map((item, index) => (
          <div key={index} className="bg-white rounded-xl p-4 shadow-sm flex items-center">
            <span className="text-2xl mr-4">{item.icon}</span>
            <div className="flex-1">
              <h3 className="font-medium">{item.title}</h3>
              <p className="text-sm text-gray-500">{item.desc}</p>
            </div>
            <span className="text-gray-400">›</span>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="max-w-md mx-auto bg-gray-50 min-h-screen">
      {/* 헤더 */}
      <div className="bg-white border-b px-4 py-3 flex items-center justify-between">
        <h1 className="text-xl font-bold">마켓플레이스</h1>
        <div className="flex gap-2 items-center">
          <button className="p-2 hover:bg-gray-100 rounded-lg">
            <Filter className="w-5 h-5" />
          </button>
          <button
            onClick={() => setShowAddProduct(!showAddProduct)}
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            <Plus className="w-5 h-5" />
          </button>
          <WalletConnect />
        </div>
      </div>

      {/* 메인 컨텐츠 */}
      <div className="flex-1">
        {activeTab === 'home' && <HomeScreen />}
        {activeTab === 'add' && <AddProductScreen />}
        {activeTab === 'profile' && <ProfileScreen />}
      </div>

      {/* 하단 네비게이션 */}
      <div className="fixed bottom-0 left-1/2 transform -translate-x-1/2 w-full max-w-md bg-white border-t">
        <div className="grid grid-cols-4 py-2">
          {[
            { id: 'home', icon: Home, label: '홈' },
            { id: 'search', icon: Search, label: '검색' },
            { id: 'add', icon: Plus, label: '등록' },
            { id: 'profile', icon: User, label: '프로필' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex flex-col items-center py-2 px-1 ${
                activeTab === tab.id ? 'text-blue-500' : 'text-gray-500'
              }`}
            >
              <tab.icon className="w-6 h-6 mb-1" />
              <span className="text-xs font-medium">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TelegramMarketplace;
